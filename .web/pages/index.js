import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Box, Button, Container, Editable, EditableInput, EditablePreview, Input, Table, TableCaption, TableContainer, Tbody, Td, Text, Th, Thead, Tr, useColorMode} from "@chakra-ui/react"
import {CheckIcon, DeleteIcon} from "@chakra-ui/icons"
import NextHead from "next/head"

const EVENT = "ws://localhost:8000/event"
export default function Component() {
const [state, setState] = useState({"category": "", "changed_quantity": "", "inv": [], "quantity": "", "text": "", "events": [{"name": "state.hydrate"}]})
const [result, setResult] = useState({"state": null, "events": [], "processing": false})
const router = useRouter()
const socket = useRef(null)
const { isReady } = router;
const { colorMode, toggleColorMode } = useColorMode()
const Event = events => setState({
  ...state,
  events: [...state.events, ...events],
})
useEffect(() => {
  if(!isReady) {
    return;
  }
  if (!socket.current) {
    connect(socket, state, setState, result, setResult, router, EVENT, ['websocket', 'polling'])
  }
  const update = async () => {
    if (result.state != null) {
      setState({
        ...result.state,
        events: [...state.events, ...result.events],
      })
      setResult({
        state: null,
        events: [],
        processing: false,
      })
    }
    await updateState(state, setState, result, setResult, router, socket.current)
  }
  update()
})
return (
<Container sx={{"padding": "1rem", "maxWidth": "900px"}}><Box><Text sx={{"fontSize": "2rem"}}>{`Welcome to Parshwa Jewellers`}</Text></Box>
<Button onClick={() => Event([E("state.get_inventory", {})])}
sx={{"marginTop": "1rem"}}>{`Get Inventory`}</Button>
<Input type="text"
placeholder="Enter Category"
onBlur={(_e) => Event([E("state.set_category", {value:_e.target.value})])}
sx={{"marginTop": "1rem", "borderColor": "#eaeaef"}}/>
<Input type="text"
placeholder="Enter Quantity"
onBlur={(_e) => Event([E("state.set_quantity", {value:_e.target.value})])}
sx={{"marginTop": "1rem", "borderColor": "#eaeaef"}}/>
<Button onClick={() => Event([E("state.add_inventory", {})])}
sx={{"marginTop": "1rem"}}>{`Add`}</Button>
<TableContainer sx={{"marginTop": "4rem"}}><Table colorScheme="yellow"
variant="striped"><TableCaption sx={{"fontSize": "1.7em"}}>{`Inventory Table`}</TableCaption>
<Thead><Tr><Th>{`Category`}</Th>
<Th>{`Quantity`}</Th>
<Th>{`Time`}</Th>
<Th>{``}</Th></Tr></Thead>
<Tbody>{state.inv.map((hgsudypp, i) => <Tr key={i}><Td>{hgsudypp.category}</Td>
<Td><Editable defaultValue={hgsudypp.quantity}
onChange={(_e) => Event([E("state.set_uppertext", {value:_e})])}
sx={{"width": "50%"}}><EditablePreview/>
<EditableInput/></Editable></Td>
<Td>{hgsudypp.created_at}</Td>
<Td><Button onClick={() => Event([E("state.edit_inventory", {category:hgsudypp.category})])}><CheckIcon/></Button></Td>
<Td><Button onClick={() => Event([E("state.delete_inventory", {category:hgsudypp.category})])}><DeleteIcon/></Button></Td></Tr>)}</Tbody></Table></TableContainer>
<NextHead><title>{`Parshwa Jewellers`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta content="favicon.ico"
property="og:image"/></NextHead></Container>
)
}