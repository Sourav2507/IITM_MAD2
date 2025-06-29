new Vue({
  el: "#find_parking_app",
  delimiters: ["${", "}"],
  data: {
    parkingLots: [],
    searchQuery: ""
  },
  methods: {
    bookspot(lot) {
      if (lot.available <= 0 || lot.requested) {
        return;
      }

      if (!confirm(`Confirm booking at "${lot.name}"?`)) return;

      fetch("/user/book_spot", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ lot_id: lot.id })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          alert("Booking confirmed!");
          lot.available -= 1;        // ✅ Update count
          lot.requested = true;     // ✅ Mark as booked
        } else {
          alert(data.message || "Booking failed.");
        }
      })
      .catch(err => {
        console.error("Error booking spot:", err);
        alert("Something went wrong.");
      });
    }
  },
  computed: {
    filteredLots() {
      const query = this.searchQuery.toLowerCase().trim();
      if (!query) return this.parkingLots;
      return this.parkingLots.filter(lot =>
        lot.address.toLowerCase().includes(query) ||
        lot.name.toLowerCase().includes(query)
      );
    }
  },
  mounted() {
    fetch("/user/find_parking_data")
      .then(res => res.json())
      .then(data => {
        this.parkingLots = data.map(lot => ({
          ...lot,
          available: Number(lot.capacity) - Number(lot.occupied),  // ✅ Fix NaN
          requested: lot.requested || false                        // ✅ Use backend flag
        }));
      })
      .catch(err => console.error("Error fetching parking data:", err));
  }
});
