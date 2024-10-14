from vanna.base import VannaBase
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
from vanna.openai import OpenAI_Chat
from openai import OpenAI
from vanna.flask import VannaFlaskApp

# client_OpenAI = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
client_OpenAI = OpenAI(base_url="http://192.168.0.54:11434/v1/", api_key="ollama")

class VannaApp(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config=config)
        # MyCustomLLM.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client_OpenAI, config=config)


vn = VannaApp(config={
    'client': QdrantClient(host='192.168.0.54', port=6333),
    'api_key': 'lm-studio',
    'model': 'qwen2.5-coder:1.5b',
    'language': 'Русский'
})

vn.connect_to_postgres(host='localhost', dbname='chat', user='postgres', password='admin', port='5432')

# vn.train(ddl="""
#     CREATE TABLE public.request (
#         id text NULL,
#         "НомерОбращения" text NULL,
#         "Дата" text NULL,
#         "Состояние" text NULL,
#         "Тип" text NULL,
#         "РабочаяГруппа" text NULL,
#         "Управление" text NULL,
#         "Услуга" text NULL,
#         "СоставУслуги" text NULL,
#         "Клиент" text NULL,
#         "Год" int8 NULL,
#         "Просрочен" text NULL,
#         vip text NULL,
#         "ТемаОбращения" text NULL,
#         "Хэштег" text NULL,
#         "ДатаВыполнения" text NULL,
#         "НормативнаяДатаЗакрытия" text NULL,
#         "Месяц" int8 NULL,
#         "ИмяМесяца" text NULL,
#         "КатегорияСостояний" text NULL,
#         "ДатаВремя" text NULL,
#         "КодЗакрытия" text NULL,
#         "ЗакрытПоШаблону" int8 NULL,
#         "НаОснованииМассового" int8 NULL,
#         "ДатаЗагрузкиДанных" text NULL,
#         "ДатаЗагрузкиДанных_last" text NULL,
#         kol_sla int8 NULL,
#         long_sla int8 NULL,
#         diff_days int8 NULL,
#         "АвтообработкаПрав" int8 NULL,
#         "ПоследнийНарядЗакрыт" int8 NULL
#     )
# """)

# # Sometimes you may want to add documentation about your business terminology or definitions.
# vn.train(documentation="Крупная IT компания обслуживает внутреннии системы и заказчиков. РабочаяГруппа - команда, подразделение, бригада. Управление - департамент, дирекция")

app = VannaFlaskApp(
    vn, 
    allow_llm_to_see_data=True, 
    title="Energo Lab SQL Chat Bot.", 
    subtitle="Заявки Итилиум", 
    logo="https://my.enplusgroup.com/local/templates/enplus/images/logo.png"
)

if __name__ == "__main__":
    app.run()
