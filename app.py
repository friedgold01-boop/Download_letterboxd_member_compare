
from urllib.parse import quote_plus

import streamlit as st


LETTERBOXD_SEARCH_BASE = "https://letterboxd.com/search/"


def clean_member(value: str) -> str:
    """Accepts handles or profile URLs and returns a clean Letterboxd handle."""
    value = value.strip()
    value = value.replace("https://letterboxd.com/", "")
    value = value.replace("http://letterboxd.com/", "")
    value = value.strip("/")
    return value.split("/")[0].strip()


def slugify_search_term(value: str) -> str:
    """
    Converts user input into Letterboxd-friendly search syntax.
    For advanced operators, Letterboxd generally expects hyphenated values:
    director:michael-mann, actor:isabelle-huppert, tag:neo-noir.
    """
    return value.strip().lower().replace(" ", "-")


def build_topic_query(topic_type: str, topic: str) -> str:
    topic = topic.strip()

    if not topic:
        return ""

    if topic_type == "Free text":
        return topic

    if topic_type == "Film / keyword":
        return topic

    if topic_type == "Director":
        return f"director:{slugify_search_term(topic)}"

    if topic_type == "Actor":
        return f"actor:{slugify_search_term(topic)}"

    if topic_type == "Cast":
        return f"cast:{slugify_search_term(topic)}"

    if topic_type == "Writer":
        return f"writer:{slugify_search_term(topic)}"

    if topic_type == "Tag / vibe":
        return f"tag:{slugify_search_term(topic)}"

    if topic_type == "Year or decade":
        return f"year:{topic.replace(' ', '')}"

    return topic


def build_letterboxd_search_url(member: str, topic_query: str) -> str:
    query = f"member:{member} {topic_query}".strip()
    return LETTERBOXD_SEARCH_BASE + quote_plus(query) + "/"


st.set_page_config(
    page_title="Letterboxd Member Compare",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 Letterboxd Member Compare")
st.caption("Compare what different Letterboxd members have written or listed about the same topic.")

st.markdown(
    """
Enter two or more Letterboxd handles, choose a topic, then open matching Letterboxd searches.

This app does **not** scrape Letterboxd. It simply builds search links using Letterboxd's own advanced search syntax.
"""
)

st.divider()

default_members = "Friedgold\n"
members_text = st.text_area(
    "Letterboxd members",
    value=default_members,
    height=140,
    help="One handle per line. You can paste profile URLs too.",
)

topic_type = st.selectbox(
    "Topic type",
    [
        "Film / keyword",
        "Director",
        "Actor",
        "Cast",
        "Writer",
        "Tag / vibe",
        "Year or decade",
        "Free text",
    ],
)

placeholder_map = {
    "Film / keyword": "Heat",
    "Director": "Michael Mann",
    "Actor": "Isabelle Huppert",
    "Cast": "Ryan Gosling",
    "Writer": "Greta Gerwig",
    "Tag / vibe": "noir",
    "Year or decade": "1970-1979",
    "Free text": "loneliness",
}

topic = st.text_input(
    "Topic",
    placeholder=placeholder_map.get(topic_type, "Heat"),
)

st.divider()

if st.button("Generate comparison links", type="primary"):
    members = [clean_member(line) for line in members_text.splitlines() if clean_member(line)]
    topic_query = build_topic_query(topic_type, topic)

    if not members:
        st.error("Add at least one Letterboxd member.")
        st.stop()

    if not topic_query:
        st.error("Add a topic.")
        st.stop()

    st.subheader("Searches")

    for member in members:
        url = build_letterboxd_search_url(member, topic_query)
        query = f"member:{member} {topic_query}"

        st.markdown(f"### @{member}")
        st.code(query, language="text")
        st.link_button(f"Open @{member} search on Letterboxd", url)

    st.divider()

    st.subheader("Quick comparison prompt")
    st.write("After opening each search, compare:")
    st.markdown(
        """
- Did both members write about the same film/person/theme?
- Who has more reviews or lists on this topic?
- Are their reactions similar or completely different?
- Is one person better for recommendations on this topic?
"""
    )

with st.expander("Example searches"):
    st.markdown(
        """
Try these:

- `member:Friedgold heat`
- `member:Friedgold director:michael-mann`
- `member:Friedgold actor:isabelle-huppert`
- `member:Friedgold tag:noir`
- `member:Friedgold year:1970-1979`
"""
    )

st.divider()
st.caption("Made for personal Letterboxd discovery. No login, no scraping, no API.")
