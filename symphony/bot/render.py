import jinja2
from jinja2 import Template

form_data = {
    "simpleForm": {
        "title": "Form-Title",
        "countries": ["america", "australia", "here"]
    }
}

def render_propose_form():
    template = Template(propose_form(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(form_data)
    print(html)
    return html

def render_review_form(message, proposer, cid, tid):
    review_data = {
        "reviewData": {
            "proposal_text": message,
            "proposer": proposer,
            "cid": cid,
            "tid": tid
        }
    }
    template = Template(review_form(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(review_data)
    return html

def review_form():
    return """
    <form id="review_form_id::{{reviewData.cid}}::{{reviewData.tid}}">
        <h2>Proposal from: {{reviewData.proposer}}</h2>
        <br/>
        <h4>{{reviewData.proposal_text}}</h4>
        <br/>
        <button name="reject_button" type="action">Reject</button>
        <button name="accept_button" type="action">Accept</button>
    </form>
"""

def propose_form():
    return """
    <form id="proposal_form_id">
        <h4>Propose to:</h4>
        <text-field name="propose_to" required="true" minlength="5" maxlength="100" />
        <h4>Proposal text:</h4>
        <textarea name="proposal" placeholder="Proposal text here" required="true"></textarea>
        <button type="reset">Reset</button>
        <button name="submit_button" type="action">Submit</button>
    </form>
"""
