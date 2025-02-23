import { useEffect, useState } from "react";
import axios from "axios";
import { Container, TextField, Button, MenuItem, Typography, List, ListItem } from "@mui/material";

function App() {
  const [investors, setInvestors] = useState([]);
  const [deals, setDeals] = useState([]);
  const [newInvestor, setNewInvestor] = useState({ name: "", email: "", phone: "" });
  const [newDeal, setNewDeal] = useState({ property_address: "", purchase_price: 0, investor_id: "" });

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/investors/")
      .then(response => setInvestors(response.data))
      .catch(error => console.error("Error fetching investors:", error));

    axios.get("http://127.0.0.1:8000/deals/")
      .then(response => setDeals(response.data))
      .catch(error => console.error("Error fetching deals:", error));
  }, []);

  const createInvestor = () => {
    axios.post("http://127.0.0.1:8000/investors/", newInvestor)
      .then(() => window.location.reload());
  };

  const createDeal = () => {
    axios.post("http://127.0.0.1:8000/deals/", newDeal)
      .then(() => window.location.reload());
  };

  return (
    <Container>
      <Typography variant="h3" gutterBottom>Real Estate Dashboard</Typography>

      <Typography variant="h5">Create Investor</Typography>
      <TextField label="Name" variant="outlined" fullWidth margin="dense"
        onChange={e => setNewInvestor({ ...newInvestor, name: e.target.value })} />
      <TextField label="Email" variant="outlined" fullWidth margin="dense"
        onChange={e => setNewInvestor({ ...newInvestor, email: e.target.value })} />
      <TextField label="Phone" variant="outlined" fullWidth margin="dense"
        onChange={e => setNewInvestor({ ...newInvestor, phone: e.target.value })} />
      <Button variant="contained" color="primary" onClick={createInvestor} sx={{ mt: 2 }}>Add Investor</Button>

      <Typography variant="h5" sx={{ mt: 4 }}>Create Deal</Typography>
      <TextField label="Property Address" variant="outlined" fullWidth margin="dense"
        onChange={e => setNewDeal({ ...newDeal, property_address: e.target.value })} />
      <TextField label="Purchase Price" type="number" variant="outlined" fullWidth margin="dense"
        onChange={e => setNewDeal({ ...newDeal, purchase_price: parseFloat(e.target.value) })} />
      <TextField select label="Select Investor" variant="outlined" fullWidth margin="dense"
        onChange={e => setNewDeal({ ...newDeal, investor_id: parseInt(e.target.value) })}>
        {investors.map(inv => (
          <MenuItem key={inv.id} value={inv.id}>{inv.name}</MenuItem>
        ))}
      </TextField>
      <Button variant="contained" color="success" onClick={createDeal} sx={{ mt: 2 }}>Add Deal</Button>

      <Typography variant="h5" sx={{ mt: 4 }}>Investors</Typography>
      <List>
        {investors.map(inv => (
          <ListItem key={inv.id}>{inv.name} - {inv.email}</ListItem>
        ))}
      </List>

      <Typography variant="h5" sx={{ mt: 4 }}>Deals</Typography>
      <List>
        {deals.map(deal => (
          <ListItem key={deal.id}>{deal.property_address} - ${deal.purchase_price}</ListItem>
        ))}
      </List>
    </Container>
  );
}

export default App;
