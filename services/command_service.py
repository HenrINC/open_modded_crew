from services.abstract_service import AbstractService
import shlex

class Service(AbstractService):
    """
    Builtin service that executes the commands
    """

    def on_post(self, posts):
        for post in posts:
            if post["type"] == "wrote_crew_wall_message":
                for comment in post["comments"]:
                    #The command's output is commented under the command post, if the post is commented, it's command has already been executed
                    if int(comment["actor"]["id"]) == self.connector.get_self_player().id:
                        break
                #If none of the comments are from self_player
                else:
                    content:str = post["content"]
                    if content.startswith("/"):
                        content = content[1:]
                        if " " in content:
                            command_name, content = content.split(" ", 1)
                            args = shlex.split(content)
                        else:
                            command_name = content
                            args = []
                        member = [i for i in self.crew.members if str(i.id) == post["actor"]["id"]][0]
                        for command in self.crew.commands:
                            if command_name == command.name:
                                try:
                                    ret = command.run(args, member)
                                except Exception as e:
                                    ret = f"ERROR: {e}"
                                if ret is None:
                                    ret = "The command returned nothing."
                                elif ret == False:
                                    continue
                                elif not isinstance(ret, str):
                                    ret = f"The command need to return a type string, not a type {type(ret)}."
                                
                                self.connector.comment_post(post["id"], ret)
    def start(self):
        self.running = True
