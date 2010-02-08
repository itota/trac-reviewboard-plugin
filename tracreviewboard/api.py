# Copyright (c) 2010, Takashi Ito
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the authors nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from genshi.builder import tag
from trac.core import *
from trac.config import Option
from trac.resource import IResourceManager
from trac.wiki import IWikiSyntaxProvider
from urlparse import urljoin


class ReviewBoardSystem(Component):

    implements(IResourceManager, IWikiSyntaxProvider)

    reviewboard_url = Option('reviewboard', 'url')

    # IResourceManager methods
    def get_resource_realms(self):
        yield 'review'

    def get_resource_url(self, resource, href, **kwargs):
        if resource.realm == 'review':
            return urljoin(self.reviewboard_url, urljoin('r/', resource.id))

    def get_resource_description(self, resource, format=None, context=None, **kwargs):
        return 'Code Review #%s' % resource.id

    # IWikiSyntaxProvider methods
    def get_wiki_syntax(self):
        return []

    def get_link_resolvers(self):
        return [('review', self._format_link)]

    def _format_link(self, formatter, ns, target, label):
        try:
            link, params, fragment = formatter.split_link(target)
            review = formatter.resource('review', link)
            return tag.a(label, href=self.get_resource_url(review, formatter.href))
        except ValueError:
            pass
        return tag.a(label, class_='missing review')

