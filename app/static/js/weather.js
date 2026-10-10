document.addEventListener("DOMContentLoaded", async () => {

    const loading = document.getElementById("weather-loading");
    const box = document.getElementById("weather-box");

    const city = document.getElementById("city");
    const temp = document.getElementById("temp");
    const desc = document.getElementById("desc");
    const humidity = document.getElementById("humidity");
    const wind = document.getElementById("wind");
    const icon = document.getElementById("icon");

    loading.innerHTML = "🌍 Loading weather...";

    if (!navigator.geolocation) {
        loading.innerHTML = "Geolocation not supported";
        return;
    }

    navigator.geolocation.getCurrentPosition(async (position) => {

        try {

            const response = await fetch("/weather", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                })
            });

            const data = await response.json();

            console.log(data);

            if (data.success) {

                loading.style.display = "none";
                box.style.display = "flex";

                city.innerHTML = data.weather.city + ", " + data.weather.country;
                temp.innerHTML = data.weather.temp + "°C";
                desc.innerHTML = data.weather.desc;
                humidity.innerHTML = "💧 " + data.weather.humidity + "%";
                wind.innerHTML = "🌬 " + data.weather.wind + " m/s";

                icon.src =
                    "https://openweathermap.org/img/wn/" +
                    data.weather.icon +
                    "@2x.png";

            } else {

                loading.innerHTML = data.message;

            }

        } catch (err) {

            console.error(err);

            loading.innerHTML = "❌ Weather loading failed.";

        }

    }, () => {

        loading.innerHTML = "📍 Please allow location.";

    });

});