from datetime import date

class Util:
    def format_attachments(self, user, questions):
        today = date.today().strftime('%b %d, %Y')
        attachments = []
        attachment = {}
        title = "*{0}* posted a status update for *{1}*".format(user['real_name'], today)

        for i in range(len(questions)):
            key = 'answer{0}'.format(i)
            answer = user[key]
            if answer:
                attachment['text'] = "*{0}*\n{1}".format(questions[i]['text'], answer)
                attachment['color'] = questions[i]['color']
                attachment['mrkdwn_in'] = ["text"]
                attachments.append(attachment)
                attachment = {}
            del user[key]
        del user['current_question']

        return title, attachments

    # http://stackoverflow.com/a/42013042/3109776
    def is_direct_message(self, output, own_id):
        return output and \
            'text' in output and \
            'channel' in output and \
            'type' in output and \
            'user' in output and \
            output['user'] != own_id and \
            output['type'] == 'message' and \
            output['channel'].startswith('D')
