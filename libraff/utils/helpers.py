import faker
from random import randint
from books.models import Book


fake = faker.Faker('az_AZ')

def fake_data_gen(number:int = 1):
    for x in range(number):
        Book.objects.create(
            author = fake.name(),
            title = fake.words(),
            price = randint(1, 150),
            like = 0,
            pdf = fake.url()
        )
    print (f'{number} fake data created')