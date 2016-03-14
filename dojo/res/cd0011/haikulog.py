import uuid
import re
import pytest

class MessageTooLongException(Exception):
	pass

class Message(object):
	MAX_LEN = 142

	def __init__(self, text):
		if len(text) > self.MAX_LEN:
			raise MessageTooLongException()

		self.uuid = uuid.uuid4()
		self.text = text
		self.mentions = self._get_mentions()

	def _get_mentions(self):
		return re.findall(r'@(\w+)', self.text)


class Twitter(object):
	def __init__(self, messages=None):
		self._messages = messages or {}

	def add_message(self, message):
		self._messages[message.uuid] = message

	def get_message(self, _uuid):
		return self._messages[_uuid]

	def get_all_messages(self):
		return self._messages.values()

	def filter(self, **kwargs):
		person = kwargs.get('mention')
		return [message for message in self._messages.values() if person in message.mentions]

def test_get_message():
	text = 'asd'
	message = Message(text)
	twitter = Twitter()
	twitter.add_message(message)
	assert text == twitter.get_message(message.uuid).text

def test_get_messages():
	text = 'asd'
	message = Message(text)
	twitter = Twitter()
	twitter.add_message(message)
	second_text = '123'
	second_message = Message(second_text)
	twitter.add_message(second_message)

	messages = twitter.get_all_messages()

	assert len(messages) == 2
	assert message in messages
	assert second_message in messages

def test_too_long_message():
	text = 'a' * (Message.MAX_LEN + 1)

	with pytest.raises(MessageTooLongException):
		Message(text)

def test_message_has_id():
	message = Message('test')
	assert message.uuid is not None

def test_message_has_content():
	message = Message('test')
	assert message.text == 'test'

def test_get_mensioned():
	message = Message('someone @john')
	assert 'john' in message.mentions

def test_get_multiple_mentioned():
	message = Message('someone @john1 @john2')
	assert 'john1' in message.mentions
	assert 'john2' in message.mentions

def test_filter_by_mentions():
	twitter = Twitter()
	message = Message('hi @john')
	twitter.add_message(message)

	assert message in twitter.filter(mention='john')
