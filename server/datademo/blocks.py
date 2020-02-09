from wagtail.core import blocks

from wagtail.images.blocks import ImageChooserBlock


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)

    cards = blocks.ListBlock(
        blocks.StructBlock([
            ("image", ImageChooserBlock(required=False)),
            ("title", blocks.CharBlock(required=False, max_length=40)),
            ("text", blocks.TextBlock(required=False, max_length=200)),
            ("button_page", blocks.PageChooserBlock(required=False)),
            ("button_url", blocks.URLBlock(required=False))
        ])
    )


    class Meta:
        template = 'streams/card_block.html'
        icon = 'placeholder'
        label = 'Staff Card'
