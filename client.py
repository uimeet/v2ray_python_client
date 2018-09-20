import sys
from v2ray.com.core.app.proxyman.command import command_pb2
from v2ray.com.core.app.proxyman.command import command_pb2_grpc
from v2ray.com.core.app.stats.command import command_pb2 as scommand_pb2
from v2ray.com.core.app.stats.command import command_pb2_grpc as scommand_pb2_grpc
from v2ray.com.core.common.protocol import user_pb2
from v2ray.com.core.common.serial import typed_message_pb2
from v2ray.com.core.proxy.vmess import account_pb2
import json
import uuid
import grpc

INBOUND_TAG = 'master_server'
SERVER_PORT = '10972'
SERVER_ADDRESS = '47.89.14.251'


def add_user(uuid, email, level=0, alter_id=32):
    print(SERVER_ADDRESS, SERVER_PORT)
    channel = grpc.insecure_channel('%s:%s' % (SERVER_ADDRESS, SERVER_PORT))
    stub = command_pb2_grpc.HandlerServiceStub(channel)

    resp = stub.AlterInbound(
        command_pb2.AlterInboundRequest(
            tag=INBOUND_TAG,
            operation=typed_message_pb2.TypedMessage(
                type=command_pb2._ADDUSEROPERATION.full_name,
                value=command_pb2.AddUserOperation(
                    user=
                    user_pb2.User(
                        level=level,
                        email=email,
                        account=typed_message_pb2.TypedMessage(
                            type=account_pb2._ACCOUNT.full_name,
                            value=account_pb2.Account(
                                id=uuid,
                                alter_id=alter_id
                            ).SerializeToString()
                        )
                    )
                ).SerializeToString()
            )
        )
    )
    print(resp)

def remove_user(uuid, email):
    channel = grpc.insecure_channel('%s:%s' % (SERVER_ADDRESS, SERVER_PORT))
    stub = command_pb2_grpc.HandlerServiceStub(channel)

    resp = stub.AlterInbound(
        command_pb2.AlterInboundRequest(
            tag=INBOUND_TAG,
            operation=typed_message_pb2.TypedMessage(
                type=command_pb2._REMOVEUSEROPERATION.full_name,
                value=command_pb2.RemoveUserOperation(
                    email=email
                ).SerializeToString()
            )
        )
    )
    print(resp)

def stat_user(email, reset = False):
    channel = grpc.insecure_channel('%s:%s' % (SERVER_ADDRESS, SERVER_PORT))
    stub = scommand_pb2_grpc.StatsServiceStub(channel)

    name = 'user>>>%s>>>traffic>>>downlink' % email

    resp = stub.GetStats(
        scommand_pb2.GetStatsRequest(
            name=name,
            reset=reset,
        )
    )
    print(resp)

def query_stat_user(email, reset = False):
    channel = grpc.insecure_channel('%s:%s' % (SERVER_ADDRESS, SERVER_PORT))
    stub = scommand_pb2_grpc.StatsServiceStub(channel)

    name = 'user>>>%s>>>traffic>>>' % email

    resp = stub.QueryStats(
        scommand_pb2.QueryStatsRequest(
            pattern = name,
            reset = reset,
        )
    )
    print(resp)


if __name__ == '__main__':
    query_stat_user('0tyf@email.com')
    #stat_user('0tyf@email.com')
    sys.exit(0)
    l = []
    for i in range(5):
        uid = uuid.uuid4().hex
        email = str(i) + 'tyf@email.com'
        add_user(uid, email)

        data = {}
        data['id'] = uid
        data['email'] = email
        data['level'] = 0
        data['alterId'] = 32
        l.append(data)

    file = open('tyf' + '.json', encoding='utf-8', mode='w')
    file.write(json.dumps(l, indent=4))

    print(json.dumps(l, indent=4))
