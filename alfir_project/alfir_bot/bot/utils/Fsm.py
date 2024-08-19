from aiogram.dispatcher.filters.state import State, StatesGroup

class AddAdminForm(StatesGroup):
    
    Contact = State()


class CreateLinkForm(StatesGroup):
    
    Link = State()
    Name = State()
    WorkersQ = State()


class ClientDataForm(StatesGroup):
    
    File = State()
    Query = State()
    FullName = State()
    Username = State()
    Bio = State()

class SetProxyForm(StatesGroup):
    
    Proxy = State()

class RelateForm(StatesGroup):
    
    Contact = State()
    Password = State()
    Code = State()