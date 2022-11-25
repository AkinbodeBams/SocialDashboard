from django.test import TestCase
from app.models import SocialDashboardData

from app.models import SocialDashboardData

class TestUpdateOrCreate(TestCase):

    def test_update_or_create_on_model_manager(self):
        SocialDashboardData.objects.update_or_create(postid=7, network="twitter",
         defaults={"network": "instagram",
            "date_posted": "2022-07-09T17:08:28Z",
            "text_content": "Second series of Turn: Washington's Spies portraits. Loyalists! (At least, as long as it suits them)  #turnamc #peggyshippen #johnandre #majorhewlett #akinbode #turnwashingtonsspies #drawingstudy #digitaldrawings #illustrationaday #mydrawings #drawingreference #drawingstagram #portraitsvisuals #digi...",
            "media_content": "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/292513311_4754661264633322_5871741416206815810_n.webp?stp=dst-jpg_e35_s1080x1080&_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=110&_nc_ohc=JScOV26ycmkAX-89oiN&edm=AOUPxh0BAAAA&ccb=7-5&oh=00_AfAKpzJahoJlRrsotZys3od9uwUDa4i29Vkznnptd2jldw&oe=63800930&_nc_sid=76ac9f",
            "language": "en",
            "sentiment": "neutral",
            "post_url": "https://www.instagram.com/p/CfzKIQiKlVf",
            "profile_name": 'https://www.instagram.com/p/CfzKIQiKlVf',
            "profile_picture": 'https://www.instagram.com/p/CfzKIQiKlVf',
            "twitter_followers": 2000,
            "engagements": {
                "likes": 75,
                "comments": 1
            }}
        )
