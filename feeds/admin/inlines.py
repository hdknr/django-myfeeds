from mytaggit.admin.inlines import GenericTaggedItemInline


class FeedTagItemInline(GenericTaggedItemInline):
    exclude = ['tag', 'value', 'users']


class EntryTagItemInline(GenericTaggedItemInline):
    exclude = ['tag', 'value', 'users']
