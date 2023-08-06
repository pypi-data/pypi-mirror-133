from __future__ import absolute_import

from collections import defaultdict

from sentry import tagstore
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.http import safe_urlopen
from sentry.integrations import FeatureDescription, IntegrationFeatures
from sentry_plugins.base import CorePluginMixin

from . import __version__, __doc__ as package_doc

class WxWorkPlugin(CorePluginMixin, notify.NotificationPlugin):
    description = package_doc
    version = __version__
    title = 'sentry-wxwork-starit'
    slug = 'sentry-wxwork-starit'
    conf_key = 'sentry-wxwork-starit'
    conf_title = title
    author = 'Sokos Lee'
    author_url = 'http://gitlab.oa.com/sokos/sentry_wxwork_notification'
    resource_links = (
        ('Bug Tracker', 'http://gitlab.oa.com/sokos/sentry_wxwork_notification'),
        ('Source', 'http://gitlab.oa.com/sokos/sentry_wxwork_notification'),
    )
    required_field = "webhook"
    feature_descriptions = [
        FeatureDescription(
            """
            Configure Sentry rules to trigger notifications based on conditions you set.
            """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]

    def is_configured(self, project):
        return bool(self.get_option('webhook', project))

    def get_config(self, project, **kwargs):
        return [
            {
                'name': 'webhook',
                'label': 'WxWork Webhook URL',
                'type': 'url',
                'placeholder': 'e.g. https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=456345234342431',
                'required': True,
                'help': 'WxWork Incoming Webhook URL'
            },
            {
                "name": "include_tags",
                "label": "Include Tags",
                "type": "bool",
                "required": False,
                "help": "Include tags with notifications",
            },
            {
                "name": "included_tag_keys",
                "label": "Included Tags",
                "type": "string",
                "required": False,
                "help": (
                    "Only include these tags (comma separated list). " "Leave empty to include all."
                ),
            },
            {
                "name": "excluded_tag_keys",
                "label": "Excluded Tags",
                "type": "string",
                "required": False,
                "help": "Exclude these tags (comma separated list).",
            },
            {
                "name": "exclude_project",
                "label": "Exclude Project Name",
                "type": "bool",
                "default": False,
                "required": False,
                "help": "Exclude project name with notifications.",
            },
            {
                "name": "exclude_culprit",
                "label": "Exclude Culprit",
                "type": "bool",
                "default": False,
                "required": False,
                "help": "Exclude culprit with notifications.",
            },
        ]

    def get_tag_list(self, name, project):
        option = self.get_option(name, project)
        if not option:
            return None
        return set(tag.strip().lower() for tag in option.split(","))

    def _get_tags(self, event):
        tag_list = event.tags
        if not tag_list:
            return ()

        return (
            (tagstore.get_tag_key_label(k), tagstore.get_tag_value_label(k, v)) for k, v in tag_list
        )

    def build_tags_widget(self, project, event):
        if not self.get_option("include_tags", project):
            return None

        tags = []
        included_tags = set(self.get_tag_list("included_tag_keys", project) or [])
        excluded_tags = set(self.get_tag_list("excluded_tag_keys", project) or [])
        for tag_key, tag_value in self._get_tags(event):
            key = tag_key.lower()
            std_key = tagstore.get_standardized_key(key)
            if included_tags and key not in included_tags and std_key not in included_tags:
                continue
            if excluded_tags and (key in excluded_tags or std_key in excluded_tags):
                continue

            tags.append({ "keyValue": { "topLabel": tag_key.encode("utf-8"), "content": tag_value.encode("utf-8") }})
        return tags

    def notify(self, notification, raise_exception=False):
        event = notification.event
        group = event.group
        project = group.project

        if not self.is_configured(project):
            return

        event_title = event.title
        event_message = event.message

        project_name = project.get_full_name()
        if group.culprit:
            culprit = group.culprit
        else:
            culprit = None

        sections = []
        widgets = []
        if not self.get_option("exclude_project", project):
            widgets.append({ "keyValue": { "topLabel": "Project", "content": project_name }})

        if not self.get_option("exclude_culprit", project) and culprit and event_title != culprit:
            widgets.append({ "keyValue": { "topLabel": "Culprit", "content": culprit }})

        times_seen = '%s times' % group.times_seen
        first_seen = '%s' % group.first_seen.strftime("%Y-%m-%d %H:%M:%S %Z")
        # widgets.append({ "keyValue": { "topLabel": "Times Seen", "content": times_seen,
        #                               "bottomLabel": first_seen }})

        # sections.append({ "widgets": widgets })

        # tags = self.build_tags_widget(project, event)
        # if tags:
        #     sections.append({ "header": "Tags", "widgets": tags })

        url = group.get_absolute_url()

        title = '[%s] %s' % (project_name, event_title)
        description = "<div class=\"highlight\">%s</div><div class=\"gray\">%s</div><div class=\"gray\">%s</div>" \
                      % (event_message, first_seen, times_seen)

        payload = {
            "msgtype": "text",
            "text": {"content": "%s \n\n报错项目：%s\n错误信息：%s \n首次出现：%s \n出现次数：%s \n查看详情： %s"
                                    % (title, project_name, event_message, first_seen, times_seen, url)}
        }

        webhook = self.get_option('webhook', project)
        return safe_urlopen(webhook, method='POST', data=json.dumps(payload))
