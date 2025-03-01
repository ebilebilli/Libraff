import faker
import random
from books.models import Book, BookCategory


fake = faker.Faker('az_AZ')

def fake_data_gen(number:int = 1):
    category_names = [
        "Roman", "Detektiv", "Elmi-fantastik", "Bioqrafiya",
        "Psixologiya", "Dini", "Tarix", "Macerə",
        "Texnologiya", "Sənədli"
    ]
    
    categories = [BookCategory.objects.get_or_create(category_name=name)[0] for name in category_names]

    for x in range(number):
        Book.objects.create(
            category = random.choice(categories),
            author = fake.name(),
            title = fake.words(),
            context = fake.sentence(),
            price = random.randint(1, 150),
            like = 0,
            pdf = fake.url()
        )
    print (f'{number} fake data created')