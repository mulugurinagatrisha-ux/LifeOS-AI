const monthYear = document.getElementById("monthYear");
const calendarBody = document.getElementById("calendarBody");

const prevBtn = document.getElementById("prevMonth");
const nextBtn = document.getElementById("nextMonth");

const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];

let currentDate = new Date();

let selectedCell = null;

function renderCalendar(){

    calendarBody.innerHTML = "";

    const year = currentDate.getFullYear();

    const month = currentDate.getMonth();

    monthYear.textContent =
        months[month] + " " + year;

    const firstDay =
        new Date(year, month, 1).getDay();

    const totalDays =
        new Date(year, month + 1, 0).getDate();

    let day = 1;

    for(let row = 0; row < 6; row++){

        const tr = document.createElement("tr");

        for(let col = 0; col < 7; col++){

            const td = document.createElement("td");

            if(row === 0 && col < firstDay){

                td.classList.add("empty");

            }
            else if(day > totalDays){

                td.classList.add("empty");

            }
            else{

                const number =
                    document.createElement("div");

                number.className =
                    "calendar-day";

                number.innerText = day;

                td.appendChild(number);

                const today =
                    new Date();

                if(
                    today.getDate() === day &&
                    today.getMonth() === month &&
                    today.getFullYear() === year
                ){

                    td.classList.add("today");

                }

                td.addEventListener(
                    "click",
                    function(){

                        if(selectedCell){

                            selectedCell.classList.remove(
                                "selected"
                            );

                        }

                        selectedCell = td;

                        td.classList.add(
                            "selected"
                        );

                    }
                );

                day++;

            }

            tr.appendChild(td);

        }

        calendarBody.appendChild(tr);

    }

}

prevBtn.addEventListener(
    "click",
    function(){

        currentDate.setMonth(
            currentDate.getMonth() - 1
        );

        renderCalendar();

    }
);

nextBtn.addEventListener(
    "click",
    function(){

        currentDate.setMonth(
            currentDate.getMonth() + 1
        );

        renderCalendar();

    }
);

renderCalendar();