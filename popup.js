chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var url = tabs[0].url;

    const btn = document.getElementById("analyze");

    if (url.includes("youtube.com/watch")){
        btn.addEventListener("click", function() {
            btn.disabled = true;
            btn.innerHTML = "Analyzing...";

            var xhr = new XMLHttpRequest();
            xhr.open("GET", "https://ytvidapi.onrender.com/analysis?url=" + url, true);
            xhr.onload = function() {
                var text = xhr.responseText;

                if (text === "0") {
                    const title = document.getElementById("title");
                    title.textContent = "Comments are turned off.";
                    btn.style.display = "none";
                    document.getElementById("icons").style.display = "none";
                    document.getElementById("score").style.display = "none";
                } else {
                    const myArray = text.split(",");
                    let positive = myArray[0].slice(0, 4);
                    let neutral = myArray[1].slice(0, 4);
                    let negative = myArray[2].slice(0, 4);
    
                    const title = document.getElementById("title");
                    title.textContent = "Video Analysis Details";
    
                    const pos = document.getElementById("positive");
                    const neu = document.getElementById("neutral");
                    const neg = document.getElementById("negative");
    
                    pos.innerHTML = positive + "%";
                    neu.innerHTML = neutral + "%";
                    neg.innerHTML = negative + "%";
    
                    const ipos = document.getElementById("pos_img");
                    const ineu = document.getElementById("neu_img");
                    const ineg = document.getElementById("neg_img");
    
                    ipos.style.display = "block";
                    ineu.style.display = "block";
                    ineg.style.display = "block";
                    btn.style.display = "none"; 
                }
            }
            xhr.send();
        });
    } else {
        const title = document.getElementById("title");
        title.textContent = "This is not a YouTube video page.";
        btn.style.display = "none";
        document.getElementById("icons").style.display = "none";
        document.getElementById("score").style.display = "none";
    }
});
