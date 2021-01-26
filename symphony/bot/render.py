import jinja2
from jinja2 import Template

form_data = {
    "simpleForm": {
        "title": "Form-Title",
        "countries": [{"name": "australia", "value": "australia-value"},
            {"name": "america", "value": "value"}]
    }
}

def render_propose_form(companies):
    template = Template(propose_form(), trim_blocks=True, lstrip_blocks=True)
    html = template.render({"companies": companies})
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
        <select name="propose_to" data-placeholder="Select Company...">
            {% for company in companies %}
                <option value="{{ company.party_id }}">{{ company.name }}</option>
            {% endfor %}
        </select>
        <h4>Proposal text:</h4>
        <textarea name="proposal" placeholder="Proposal text here" required="true"></textarea>
        <button type="reset">Reset</button>
        <button name="submit_button" type="action">Submit</button>
    </form>
"""
