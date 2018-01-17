from mock import patch
from nose.tools import eq_, ok_

from site_up_checker import page_validator as pv


def test_get_raw_text_from_html():
    # define input and expected output
    html_doc = "<html>" \
        "<head>" \
        "<meta charset=\"utf-8\">" \
        "</head>" \
        "<body>dummy content</body>" \
        "<script>some javascript code</script></html>"

    expected = "dummy content"

    # run test
    result = pv.get_raw_text_from_html(html_doc)

    # check output
    eq_(result, expected)


@patch("site_up_checker.page_validator.get_raw_text_from_html")
def test_check_page(mock_get_raw):
    mock_get_raw.return_value = "Maps YouTube Log In"

    html_doc = ""   # this is mocked anyway
    # testcase 1, all requierements are met
    requirements = ["Maps", "YouTube"]
    result = pv.check_page(html_doc, requirements)

    # check if result equals True
    ok_(result)

    # testcase 2, not all requierements are met
    requirements = ["Maps", "RandomWord"]
    result = pv.check_page(html_doc, requirements)
    # check if result equals False
    ok_(not result)

