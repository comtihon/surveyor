import json
from time import sleep

from colorama import Fore
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord


class Kafka:
    def __init__(self, conf: dict) -> None:
        super().__init__()
        self._host = conf['host']
        self._port = str(conf['port'])
        self._topic = conf['topic']

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> str:
        return self._port

    @property
    def topic(self) -> str:
        return self._topic

    def connect_consumer(self, host, port, topic, retry=True):
        try:
            return KafkaConsumer(topic,
                                 group_id='tester',
                                 bootstrap_servers=host + ':' + port,
                                 auto_offset_reset='earliest',
                                 api_version=(0, 10, 1))
        except:
            if retry:
                sleep(5)
                return self.connect_consumer(host, port, topic, False)
            print(Fore.RED + 'No kafka brokers available')
            raise Exception('No kafka brokers available')

    def check_answers(self, answers_selected: list) -> bool:
        print('Checking answers in kafka', end=' ')
        consumer = self.connect_consumer(self.host, self.port, self.topic)
        streamed_answeres = self.get_messages(consumer)
        if streamed_answeres is None or streamed_answeres == {}:
            print(Fore.RED + 'No answeres streamed to kafka')
            return False
        for (q, a) in answers_selected:
            if q not in streamed_answeres or streamed_answeres[q] != a:
                print(Fore.RED + 'No ' + str((q, a)) + ' in kafka')
                print(streamed_answeres)
                return False
        print(Fore.GREEN + 'OK')
        return True

    def get_messages(self, consumer) -> dict:
        consumer_records = consumer.poll(10000).values()
        records = [item for sublist in consumer_records for item in sublist]
        list_of_dicts = [Kafka.parse_value(c) for c in records]
        streamed = {}
        for d in list_of_dicts:
            streamed[d['questionId']] = d['answerId']
        return streamed

    @staticmethod
    def parse_value(c: ConsumerRecord) -> dict:
        return json.loads(c.value.decode())
