const app = Vue.createApp({
    data() {
        return {
            cookies: [], 
            query: ""
        };
    }, 
    methods: {
        getCookies() {
            let query = encodeURIComponent(this.query);

            if (query === "") {
                axios.get("/cookies")
                    .then((response) => {
                        if (response.data.code === 200) {
                            this.cookies = response.data.data; 
                        }
                    });
            } else {
                axios.get(`/cookies/${query}`)
                    .then((response) => {
                        if (response.data.code === 200) {
                            this.cookies = response.data.data; 
                        }
                    });
            }
        }, 
        updateSearch() {
            let query = encodeURIComponent(this.query);

            axios.get(`/cookies/${query}`)
                .then((response) => {
                    if (response.data.code === 200) {
                        this.cookies = response.data.data; 
                    }
                });
        }, 
        clearAll() {
            this.query = "";

            axios.delete(`/cookies`)
                .then((response) => {
                    this.getCookies();
                });
        }
    }, 
    created() {
        axios.get("/cookies")
            .then((response) => {
                if (response.data.code === 200) {
                    this.cookies = response.data.data; 
                }
            });
    }
});

app.mount("#app");