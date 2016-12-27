# -*- coding: utf-8 -*-
import logging
from copy import copy

from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartnerGetStudios(common.TransactionCase):
    """Test Suite for the gets of res.partner."""

    def setUp(self):
        """Build the partners for each tests."""
        super(TestResPartnerGetStudios, self).setUp()
        self.values = {
            'name': 'tname',
            'is_company': True,
            'image': self.__base64Image(),
            'street': '8017 Avenue Chateaubriand',
            'zip': 'H2R 2M7',
            'city': 'Montreal',
            'country_id': 39,  # Canada
            'website': 'http://www.cgstudiomap.org',
        }

        self.partner_pool = self.env['res.partner']
        # to avoid to have google checks to be triggered.
        self.partner_pool.__dryRun__ = True
        self.company_pool = self.env['res.company']
        self.company = self.company_pool.browse(1)
        self.__partners = self.__build_partners()

    def tearDown(self):
        """Clean the partners that were created in the setUp."""
        for partner in self.__partners:
            partner.unlink()

        self.partner_pool.__dryRun__ = False

    def test_dryRun_on(self):
        """Double check the mode dryRun of partner poll is on."""
        self.assertTrue(self.partner_pool.__dryRun__)

    def test_partnersAreCreated(self):
        """Check the partners for the tests are created as expected."""
        self.assertTrue(
            self.__partners,
            'No partners were created for the test!'
        )

    def test_getStudioFromSameLocation_cgstudiomapIsNotInIt(self):
        """Check that the partner related to the company
        cgstudiomap is not in the list of partners.
        """
        partners = self.partner1.get_studios_from_same_location()
        self.assertTrue(
            all(partner.id != self.company.partner_id.id
                for partner in partners)
        )

    def test_getStudioFromSameLocation_partnerIsNotInIt(self):
        """Check that the partner the request is done against is not in the
        list.
        """
        partners = self.partner1.get_studios_from_same_location()
        self.assertTrue(
            all(partner.id != self.partner1.id for partner in partners)
        )

    def test_getStudioFromSameLocation_isCompany(self):
        """Check that the all partners are companies and that the not company
        partner is exclude.
        """
        values = copy(self.values)
        values['is_company'] = False
        partner = self.partner_pool.create(values)
        partners = self.partner1.get_studios_from_same_location()
        self.assertNotIn(partner, partners)
        self.assertTrue(
            all(partner.is_company for partner in partners)
        )

    def test_getStudioFromSameLocation_image(self):
        """Check that the all partners have image and the partner without
        image is excluded.
        """
        values = copy(self.values)
        values['image'] = False
        partner = self.partner_pool.create(values)
        partners = self.partner1.get_studios_from_same_location()
        self.assertNotIn(partner, partners)
        self.assertTrue(
            all(partner.image for partner in partners)
        )

    def test_getStudioFromSameLocation_country(self):
        """Check that the all partners have the same country than the witness
        partner and partner with different countries are excluded.
        """
        values = copy(self.values)
        values['country_id'] = 33
        partner = self.partner_pool.create(values)
        partners = self.partner1.get_studios_from_same_location()
        self.assertNotIn(partner, partners)
        self.assertTrue(
            all(partner.country_id.id == self.partner1.country_id.id
                for partner in partners)
        )

    def test_getStudioFromSameLocation_active(self):
        """Check that the all partners are active, and the inactive
        partner is excluded.
        """
        values = copy(self.values)
        values['active'] = False
        partner = self.partner_pool.create(values)
        partners = self.partner1.get_studios_from_same_location()
        self.assertNotIn(partner, partners)
        self.assertTrue(
            all(partner.active for partner in partners)
        )

    def test_getStudioFromSameLocation_open(self):
        """Check that the all partners are with status open, and the partner
        with the status closed is excluded.
        """
        values = copy(self.values)
        values['state'] = 'closed'
        partner = self.partner_pool.create(values)
        partners = self.partner1.get_studios_from_same_location()
        self.assertNotIn(partner, partners)
        self.assertTrue(
            all(partner.state == 'open' for partner in partners)
        )

    def __build_partners(self):
        """Build a set of partners to tests against."""
        # 3 partners from the same location.
        self.partner1 = self.partner_pool.create(self.values)
        self.partner2 = self.partner_pool.create(self.values)
        self.partner3 = self.partner_pool.create(self.values)
        self.partner4 = self.partner_pool.create(self.values)
        self.partner5 = self.partner_pool.create(self.values)
        self.partner6 = self.partner_pool.create(self.values)
        return [
            self.partner1,
            self.partner2,
            self.partner3,
            self.partner4,
            self.partner5,
            self.partner6,
        ]

    @staticmethod
    def __base64Image():
        """Return an image under base64 code."""
        return (
            "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"
            "qI+pf3/T8+ZYg1lDV6NKY22TUFNxM745rQVqSWhZveV/a6bVpXXo9r7bXW3qbc3tU"
            "u2Vdwh3iu4y3z13D3Pv+L3d+4n31zvCO1Y6/Trnuzy6Jh84P3j+0OZh/yOzR08eGz"
            "1+0K3bff+J5pM7T9We3u5R6bn1TOlZS69ib3OfYl9zv1J/y4DyQOug6mDbkMbQvWH"
            "t4c4Rg5HHz02fPxu1HB0acxibGHcbn5nwnnj3IvjF55exL7cnk6eQU2nT9NN5r7he"
            "lb8WfV03ozRzd9ZgtnfObm5ynjy//CbqzY+F429xb/MWeRer38m9u7NktDT4fv/7h"
            "eXw5e2V1A8MH4o/inxs+qTzqXfVeXXhc+Tn3S9n1tjXKr8qfO1at15/9S3k2/ZG2i"
            "b7ZtV3le/dW05bi9txP9A/CnZEd9p+mv2c2g3Z3Q0nRZJ+LwXglA3m6wvAl0oAcC4"
            "A4AcBwND+s17+T4FTFh8wyt4RkoKWYSVwd4QoEo38jFpCj1O9pp7FbGCROCKtGV00"
            "fSnDOJ6GSYs5kaWOdZFdjIPEmc81wIPkVeTzIWTwNwgMC34kwoRpRehEaShvvu/iH"
            "yRmJUekHkg3y1yRzZQ7LB+o4KiooySmjFf+obKg2qvWpF6scUwzUMtWW0tHQpdXj0"
            "Wf3oDaEGG4Y7RhvGryznRm34RZv/kjizuWjVY3rK/ZVNtes7thX+dw07HRqdG5yaX"
            "JtXF/g9vNA3XudR4Nnq2kTq9e8gvvtz5ffXf9aQJYAvmDxIMVQ7RDTcMcwn0i4iLP"
            "RlVE34+ZiP0cT53Al6h80PIQ+XD8kbSk/OTSo2Upl44VHD93IjX14MmIU76nXdMs0"
            "3XPKJ4VyeA6x5hJk0WdTXOePoctl5Annq9QoHnBsNCiyKF4fwn5YtCl6NLksszyss"
            "vNV3quvq74WkVVzXVNukbvusMNv9r4ulP1eTfLG2oaG5vamu+3PLr1tLXv9lDbaPv"
            "Encm7r++9ub/csd4Ff8D8UOSRxmPrbvKTuKdpPcXP6no7+4b6ZwY+DK4PbQ3/GNl+"
            "vjm6PvZ5/ANltM2/fDU5MTU83ffqyetHM49ne+aG56ffLC2sL0LvsEts7wWWpVZUP"
            "+h/NP1ktmrwWe4L65cva91fL6wHfdPYoN14vVn3PXnLZpuw/flH507WT89dmd3df8"
            "m/FJIPuUbJ/3uqOerPNBisEM6Q1p/uHH0XwxpeksmD+QLLczYcuwXHCc4Orm884rw"
            "efGcITfxjAl+F6IhcwkQRgiibGI3YpvicRL9km9Rl6TMysbKecqbyMgqsCjuKb5R6"
            "lOtUclQT1dzV9TSImlSay1pD2q06l3Wz9FL04wyCDb2MHI3NTLRMZfcJmDGbo803L"
            "d5bTlkNWT+x6bK9Z9du3+rQ7FjvVONc4VLmWrg/x+3sgZPuKR5JnkmkFK808nnvYp"
            "9K33q/Vv+OgCeBA0GjwVMhb0JXwjYjUJGsURLRejHOsaFxx+LzE64n3j84fOjN4fU"
            "kWDLmKG0K9hjq2M/jX08spU6fHDr16HRrWk36xTOZZ1My4s6FZPpl+WUHno/MScw9"
            "lpeef76g6EJ5YXVRfXFzyZ2LXZeelY6VvSlfv4K6ylYhVqlRZVntcS28Jvl65o3S2"
            "rq6u/U9N0cbXje+a1pt3mzZbUXdxrUxtXPc4btLvCdxX75Ds3Nfl8uD4IdJj84/ru"
            "xue9L3dKbnSy+ij6WfOKA4qDdkPmw34vTcddRtzH3cY8LzhedL0iRpijRNekV6TZ7"
            "xnw2fOzSf9qZwoeZt+2Lvu+mlD+9/rGA/cHwkfpJalf4sTBkBu2uzXzvXS78d2XDb"
            "VPvO9v3b1sh2/Y+zO4E/jXYF/lv+/3399+MxTBrMUZT6/0SpfzJnEddzHhyvBl8QI"
            "Z//nsCc4E8igzBBRExUVExYnCDBIUkvRS0NpNdkFmUn5J7ItyhUKOYqHVOOUDmgaq"
            "amrC6gQauxqTmvNajdodOoW6VXql9kkGuYYXTSONkk3jR8n5+Zu7m9hamllpWStbS"
            "NqC3RTtCe34HgyOvE5czuwuLKuB/rhj4AHdhx/+6x4blJ2ibDvKl86HxZ/Lj8CQHE"
            "QLEg6WC5EMVQ1TDtcOMIm0iPqPDo5Jis2LK4m/EdCQOJ0weXD20egSVhkrFHqVMgy"
            "iz65vjzE12pdSdLTqWdjkkjpVucUTkrkEGXsXPuQ+Zc1lT2xPnxnIncF3kT+RMF4x"
            "fGCp8XjRQPlQxc7LvUXzpUNlY+TZnpVq9uVSKqcNXM13hqiNelbijUqtVp1+vfNGg"
            "wbDRo0mvWadG8pdaqfFu+Tbpd/A7xLv89nvucHZydPF2CDyQfKj/Se2zR7fTE62lw"
            "T+yzpN5TfVn9BQMXB8uGyodLR4qf549mjaWPH584/CLuZdik/5TntMsru9fWMzazT"
            "nNe8xFvUhZy31Yttr/rW5p5/2UF8YHpo+AnuVXNzwZfjNaMvuqva39T31DalP0uvk"
            "Xc5vvBvoP/idtF/cr/P99NfgmK0lNeocwTDicBMM8C4KI6AEQMAFhaAKxxANirApj"
            "eOQCTlwcwmct78wdEaTypAT1gAwQgDpQp/bEN8ABhIInSU5aDZvAUTIM1CAMRIDXI"
            "HgqD0qBK6DG0AEPBRGDmlF6vgNLfrcDZ4SbwRHgd/B1CkNKpXUG8Q0pRerEuFB3KE"
            "9WIpkJ7otup2KjiqV5Sa1NXUvqkI5gPNB40Q1gD7C2cGO4iLTPtWToquhP0SPqTDF"
            "iG84zcjNV4ZXw3kxPTInMCCw1LKasy6yBbMDuGvYbDkuMrZzGXMdcadymPBc8WbyW"
            "fAwFJaOEPFCAIvBTMFbIl4omjwoUinqLCoh/EGsUTJLQlUZIDUkXS/jIqsjSyr+Va"
            "5DMVghXNleSUeVTwqrRq9OqsGgRNaS1tbTudQN3jemX6nQbzRmhjMRMz04B9J8xKz"
            "dstJiw3rNltNG197M7ZtzssU8aylUuKa9P+hQMs7kYecZ41pBkyu7edT5bvkD8+wD"
            "mwNGglRD00I2wxwjCyMhoXExf7Jt4+ofug5qGWI3JJ9UdlUxqOy5+4eVLyVEUaT3r"
            "BWXxGViZDVs55jpzyPMn89gsWhfPFSRcFLg2WnbisexVe8bQq+5rHdZlaeN3Lm02N"
            "Wc0Rt2xuy7TT3Jm719yR2uX8UOIxrHvyacuz3L7YAdchvRGZUZFxuRcOkwXT2zOxc"
            "z8WTr5jfX/9g9GnN19OrktvTG1l7Bj8fn/8yT/r7/wrUfJvDdxBCDgMMkApaASPwS"
            "RYhdAQD6QMWUNBUCp0GeqEZmAQTABmBAuCZcPaYW/heLgePAZ+Df4GQUCQEFcRK0g"
            "FZBKyD8WNCkM9RHOhY9EjlF46h+o7tSd1D0YZU0HDTnMWC8cmYj/jAnCztPtpx+kc"
            "6cbp99PPMQQxbDCewLPgq5m0mEaYA5h3WfJZZVn7KNmnZW/gcOaEcdZyuXHjuO/zR"
            "PIK8U7wpRE0CV/4qwRIgtyCk0JFRHdhQeFlkWbRZDFzcVbxeYlayQQpI2km6QWZVt"
            "kMOR95HQUuhW3FaaUHlPmsTLVQrUi9XKNW8y7lffZWZ1ePU1/NwM3wqFG18ZDJ930"
            "8ZtrmHhaHLUus7lnP2VLbydm7O5x1vOe05iLq6rW/yG3EHeOh6xlPuum17C3i4+db"
            "7fchQCHwSFBPCHtoUFhHBHtkbNR4jEbslXi6hMOJHw+RDk8k2ST3pZgf6zthnTp8y"
            "vb0ULrlmZ4Mk3PdWabZ/TkOua/ygwq2Cs8UE0raL7mU/iyvueJewVr5vDq3xvUGoX"
            "al/nZDWpN7i0Ir7vZi+/27Ofd9OhUegId9j4ufhPTo9LL2rQ70DtWMZIzGjvu98Jt"
            "MnK58vTyn+6Z8EbMUs7zw0XV1eM1qfXDTcev1Tsi/5P/f1/+r3/XP/7v+Q3/X/yNK"
            "/SNhwjAzWDgsH3Yf9h7OAjeEx8Fr4HMIboQrohAxhSQg/ZD1yB+ofagi1Ce0IboEv"
            "UnlQNVMzUp9iHoeY4FpoxGhKcBSUUbACs4D95zWnPYxnR5dJ70e/WMGc4ZRRhLjJ/"
            "wRJlqmUmY55scsbixfWc+xSbD1sody4DnaOX24GLk6uMN5+HgGeY/yyfG9JRTx2wn"
            "QCjwTTBeyIDIQXwiXi4SIqoohxYbESyQCJJWl0FIvpGtlTsi6y6nJs8tvKbxS7FZq"
            "Vq5RqVKtVWtX79WY1dzSZtFR1HXWO6JfaTBiBDeWNyGbZu5rM5uzoLaUtXK1Pmlzy"
            "3bJnsfByTHbadCF3tVuf57bhDuHx37PYtIrsoB3oE+TH+RvHVAeuBFsFVIThgkPiR"
            "iN0otuiBWOK03gSiw6xHW4PEksuTlF/9jzE/6pP05lphHS689qZjzNdMx6ez4+F5t"
            "3pUDrwmTRwRKeiw9Lw8p5L49dza10rRa6tn79Se2l+oQGpyblFs5W2O2V9vG7nfcr"
            "O1MfeDyS7YaeDPaU9kb2Gw/yDn0fGRttGS98cXQydNrrtces33zCwvnFxqWJFfBRf"
            "NX1y5mvXd+2vytvx+7c/pX/KF95ud/TB4TVAwD5and3jQgAOhuAnazd3e3y3d2dy5"
            "RmYwqAjuB/vsX/nmvoAcgmsrKhxPqm2P/HN/H/AMfkXNDgtxjcAAABm2lUWHRYTUw"
            "6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczpt"
            "ZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuc"
            "zpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucy"
            "MiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICA"
            "gICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyI+CiAg"
            "ICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj43MjwvZXhpZjpQaXhlbFhEaW1lb"
            "nNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj42NjwvZXhpZjpQaX"
            "hlbFlEaW1lbnNpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjp"
            "SREY+CjwveDp4bXBtZXRhPgpiWMscAAAJlUlEQVR4AeVbPW8VRxRdI1rMDzA/IOYH"
            "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"
            "YAAAAASUVORK5CYII="
        )
