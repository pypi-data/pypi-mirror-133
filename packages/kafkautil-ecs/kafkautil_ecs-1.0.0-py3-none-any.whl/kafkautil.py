import click
from kafka import KafkaConsumer,KafkaAdminClient,KafkaProducer

@click.group()
def cli():
    pass

@cli.command()
@click.argument('bootstrap_server')
def test_connection(bootstrap_server):
    """ BOOTSTRAP_SERVER: Server address for kafka topic """
    click.echo(f"\nTesting Connectivity: {bootstrap_server}\n")
    click.echo("--- Kafka Admin Information ---\n")
    admin_client = KafkaAdminClient(bootstrap_servers=[bootstrap_server])
    click.echo("Current Kafka Topics List:\n")
    click.echo(f"{admin_client.list_topics()}\n")
    click.echo("Kafka Topics Description:\n")
    click.echo(f"{admin_client.describe_topics()}\n")

@cli.command()
@click.argument('bootstrap_server')
@click.argument('topic')
@click.option('--offset',default='earliest',help='Offset can be earliest or latest')
def read_data(bootstrap_server,topic,offset):
    """ BOOTSTRAP_SERVER: Server address for kafka topic\n
        TOPIC: Kafka topic Name
    """
    consumer = KafkaConsumer(topic,auto_offset_reset=offset, bootstrap_servers=[bootstrap_server
                                                                                ],api_version=(0, 10, 0))
    msg_pack = consumer.poll(timeout_ms=100000)
    for tp, messages in msg_pack.items():
        for message in messages:
            incomingKafkaMessage = message.value.decode('utf-8')
            click.echo(incomingKafkaMessage)

@cli.command()
@click.argument('bootstrap_server')
@click.argument('topic')
@click.option('--message',default='test message',help='Test message to send')
def send_data(bootstrap_server,topic,message):
    """ BOOTSTRAP_SERVER: Server address for kafka topic\n
        TOPIC: Kafka topic Name
    """
    producer = KafkaProducer(bootstrap_servers=[bootstrap_server])
    producer.send(topic, message.encode())
    producer.flush() 
    click.echo(f"Message Sent to {bootstrap_server} @ topic {topic} with message {message}")

if __name__ == '__main__':
    cli()