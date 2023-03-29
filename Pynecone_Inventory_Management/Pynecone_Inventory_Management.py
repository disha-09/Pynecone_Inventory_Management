# Import pynecone.
from datetime import datetime
from .db import Inventory
import pynecone as pc

class State(pc.State):
    """The app state."""

    text: str = ""
    inv: list[Inventory] = []
    category: str = ""
    quantity: str = ""
    changed_quantity: str = ""

    def set_uppertext(self, value):
        self.changed_quantity = value
    
    def edit_inventory(self, category:str):
        if self.changed_quantity == "":
            return self.get_inventory()
        with pc.session() as session:
            session.query(Inventory).filter_by(category=category).update({'quantity': self.changed_quantity})
            session.query(Inventory).filter_by(category=category).update({'created_at': datetime.now().strftime("%B %d, %Y %I:%M %p")})
            session.commit()
        self.changed_quantity = ""
        return self.get_inventory()
    
    def delete_inventory(self, category:str):
        with pc.session() as session:
            session.query(Inventory).filter_by(category=category).delete()
            session.commit()
        return self.get_inventory()
    
    
    def add_inventory(self):
        if self.category == "" or self.quantity == "":
            return self.get_inventory()
        with pc.session() as sess:
            if sess.query(Inventory).filter_by(category=self.category).all():
                return pc.window_alert("Category already exists")
            sess.add(
                Inventory(
                    category=self.category, quantity=self.quantity, created_at=datetime.now().strftime("%B %d, %Y %I:%M %p")
                )
            )
            sess.commit()
        return self.get_inventory()
    
    def get_inventory(self) -> list[Inventory]:
        with pc.session() as session:
            # print("All...")
            self.inv = session.query(Inventory).all()
            # print(self.inv)
    

# Define views.

def header():
    """Basic instructions to get started."""
    return pc.box(
        pc.text("Welcome to Pynecone Inventory System", font_size="2rem"),
        # pc.text(
        #     "Inventory Management System!",
        #     margin_top="0.5rem",
        #     color="#666",
        # ),
    )

def inv_row(inv: Inventory):
    return pc.tr(
        pc.td(inv.category),
        # pc.td(inv.quantity),
        pc.td(
            pc.editable(
                pc.editable_preview(),
                pc.editable_input(),
                default_value=inv.quantity,
                # submit_on_blur = True,
                on_change=lambda: State.set_uppertext,
                width="50%",
            )
        ),
        pc.td(inv.created_at),
        pc.td(
            pc.button(
                pc.icon(tag="check"),
                on_click=lambda: State.edit_inventory(inv.category),
                # bg="red",
                # color="white"
            )
        ),
        pc.td(
            pc.button(
                pc.icon(tag="delete"),
                on_click=lambda: State.delete_inventory(inv.category),
                # bg="red",
                # color="white"
            )
        )
    )

def index():
    """The main view."""
    return pc.container(
        header(),
        pc.button("Get Inventory", on_click=State.get_inventory,margin_top="1rem"),
        pc.input(
            placeholder="Enter Category",
            on_blur=State.set_category,
            margin_top="1rem",
            border_color="#eaeaef",
        ),
        pc.input(
            placeholder="Enter Quantity",
            on_blur=State.set_quantity,
            margin_top="1rem",
            border_color="#eaeaef",
        ),
        pc.button("Add", on_click=State.add_inventory, margin_top="1rem"),
        pc.table_container(
            pc.table(
                pc.table_caption("Inventory Table",font_size="1.7em"),
                pc.thead(pc.tr(
                    pc.th("Category"),
                    pc.th("Quantity"),
                    pc.th("Time"),
                    pc.th("")
                )),
                pc.tbody(pc.foreach(State.inv, inv_row)),
                variant="striped",
                color_scheme="yellow",
            ),
            margin_top="4rem",
        ),
        padding="1rem",
        max_width="900px",
    )

# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="Parshwa Jewellers")
app.compile()