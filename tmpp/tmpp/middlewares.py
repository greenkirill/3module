# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.spidermiddlewares.offsite import OffsiteMiddleware, URLWarning
import re
import warnings

class MyOffsiteMiddleware(OffsiteMiddleware):
    def get_host_regex(self, spider):
        allowed_domains = getattr(spider, 'allowed_domains', None)
        if not allowed_domains:
            return re.compile('') # allow all by default
        url_pattern = re.compile("^https?://.*$")
        for domain in allowed_domains:
            if url_pattern.match(domain):
                warnings.warn("allowed_domains accepts only domains, not URLs. Ignoring URL entry %s in allowed_domains." % domain, URLWarning)
                
        regex = r'^(%s)$' % '|'.join(re.escape(d) for d in allowed_domains if d is not None)
        return re.compile(regex)