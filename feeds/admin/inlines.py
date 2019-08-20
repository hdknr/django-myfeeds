from mytaggit.admin.inlines import GenericTaggedItemInline


class EntryTagItemInline(GenericTaggedItemInline):
    exclude = ['tag', 'value', 'users']
