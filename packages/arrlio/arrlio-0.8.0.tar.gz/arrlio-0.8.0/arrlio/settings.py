from typing import List, Optional

from pydantic import BaseSettings, Field

from arrlio.tp import BackendT, PositiveIntT, PriorityT, TimeoutT


BACKEND = "arrlio.backend.local"

TASK_BIND = False
TASK_QUEUE = "arrlio.tasks"
TASK_PRIORITY = 1
TASK_TIMEOUT = 300
TASK_TTL = 300
TASK_ACK_LATE = False

RESULT_TTL = 300
RESULT_RETURN = True
RESULT_ENCRYPT = False

MESSAGE_EXCHANGE = "arrlio.messages"
MESSAGE_PRIORITY = 1
MESSAGE_TTL = 300
MESSAGE_ACK_LATE = False

CONSUMER_TASK_QUEUES = [TASK_QUEUE]
CONSUMER_MESSAGE_QUEUES = [MESSAGE_EXCHANGE]
CONSUMER_POOL_SIZE = 100


class TaskConfig(BaseSettings):
    bind: bool = Field(default_factory=lambda: TASK_BIND)
    queue: str = Field(default_factory=lambda: TASK_QUEUE)
    priority: PriorityT = Field(default_factory=lambda: TASK_PRIORITY)
    timeout: Optional[TimeoutT] = Field(default_factory=lambda: TASK_TIMEOUT)
    ttl: Optional[PositiveIntT] = Field(default_factory=lambda: TASK_TTL)
    ack_late: Optional[bool] = Field(default_factory=lambda: TASK_ACK_LATE)
    result_return: Optional[bool] = Field(default_factory=lambda: RESULT_RETURN)
    result_encrypt: Optional[bool] = Field(default_factory=lambda: RESULT_ENCRYPT)

    class Config:
        validate_assignment = True
        env_prefix = "ARRLIO_TASK_"


class ResultConfig(BaseSettings):
    ttl: Optional[PositiveIntT] = Field(default_factory=lambda: RESULT_TTL)

    class Config:
        validate_assignment = True
        env_prefix = "ARRLIO_RESULT_"


class MessageConfig(BaseSettings):
    exchange: str = Field(default_factory=lambda: MESSAGE_EXCHANGE)
    priority: PriorityT = Field(default_factory=lambda: MESSAGE_PRIORITY)
    ttl: Optional[PositiveIntT] = Field(default_factory=lambda: MESSAGE_TTL)
    ack_late: Optional[bool] = Field(default_factory=lambda: MESSAGE_ACK_LATE)

    class Config:
        validate_assignment = True
        env_prefix = "ARRLIO_MESSAGE_"


class ProducerConfig(BaseSettings):
    backend: BackendT = Field(default_factory=lambda: BACKEND, env="ARRLIO_BACKEND")
    task: TaskConfig = Field(default_factory=TaskConfig)
    result: ResultConfig = Field(default_factory=ResultConfig)
    message: MessageConfig = Field(default_factory=MessageConfig)

    class Config:
        validate_assignment = True
        env_prefix = "ARRLIO_PRODUCER_"


class ConsumerConfig(BaseSettings):
    backend: BackendT = Field(default_factory=lambda: BACKEND, env="ARRLIO_BACKEND")
    task_queues: List[str] = Field(default_factory=lambda: CONSUMER_TASK_QUEUES)
    message_queues: List[str] = Field(default_factory=lambda: CONSUMER_MESSAGE_QUEUES)
    pool_size: PositiveIntT = Field(default_factory=lambda: CONSUMER_POOL_SIZE)

    class Config:
        validate_assignment = True
        env_prefix = "ARRLIO_CONSUMER_"
