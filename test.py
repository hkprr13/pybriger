from pybridger import *

engine = Engine(
    sqlEngineName = "mysql",
    hostName      = "localhost",
    userName      = "root.KazuhiroKondo",
    password      = "qazxsw@12#",
    database      = "pybrigertestdb"
)
engine.launch()

class User(Model):
    id         = Column(Integer(), isPrimaryKey = True, isAutoIncrement= True)
    name       = Column(VarChar(50))
    email      = Column(VarChar(100))
    age        = Column(Integer())


class Post(Model):
    id         = Column(Integer(), isPrimaryKey = True)
    user_id    = Column(Integer(), foreignKey   = ForeignKey("User.id"))
    title      = Column(VarChar(100))
    content    = Column(Text())


class Comment(Model):
    id         = Column(Integer(), isPrimaryKey = True)
    post_id    = Column(Integer(), foreignKey   = ForeignKey("Post.id"))
    user_id    = Column(Integer(), foreignKey   = ForeignKey("User.id"))
    content    = Column(Text())


engine.select(User, User.id, User.name).innerJoin(
    Post, (User.age == Post.user_id) & (Comment.id == Post.title) 
) 

