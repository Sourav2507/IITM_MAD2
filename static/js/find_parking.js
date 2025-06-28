new Vue({
    el: "#find_parking_app",
    delimiters: ["${", "}"],
    data: {
        parkingLots: [],
        searchQuery: ""
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
                this.parkingLots = data;
            })
            .catch(err => console.error("Error fetching parking data:", err));
    }
});