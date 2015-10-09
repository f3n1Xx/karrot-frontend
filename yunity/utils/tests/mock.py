from factory import DjangoModelFactory, CREATE_STRATEGY, LazyAttribute, post_generation, SubFactory

from yunity.models import Category
from yunity.utils.tests.fake import faker


class Mock(DjangoModelFactory):
    class Meta:
        strategy = CREATE_STRATEGY
        model = None
        abstract = True


class MockCategory(Mock):
    class Meta:
        model = "yunity.Category"
        strategy = CREATE_STRATEGY


class MockUser(Mock):
    class Meta:
        model = "yunity.User"
        strategy = CREATE_STRATEGY

    is_active = True
    is_staff = False
    type = Category.objects.get(name='user.default')
    display_name = LazyAttribute(lambda _: faker.name())
    email = LazyAttribute(lambda _: faker.email())
    password = LazyAttribute(lambda _: faker.password())
    locations = LazyAttribute(lambda _: [faker.location() for _ in range(2)])


class MockChat(Mock):
    class Meta:
        model = "yunity.Chat"
        strategy = CREATE_STRATEGY

    administrated_by = SubFactory(MockUser)

    @post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for participant in extracted:
                self.participants.add(participant)
