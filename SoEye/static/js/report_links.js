// Add event listener to evidnce to make it clickable
const evidence = document.getElementsByClassName('evidence')

console.log(evidence.length)
for (i=0; i < evidence.length; i++) {
    let data = i.toString()
    evidence[i].addEventListener('click', () => {
        $.ajax({
            type: "POST",
            contentType: "text; charset=utf-8",
            url: "/remove_evidence",
            data: data,
            dataType: "text"
        })
        location.reload();
    })
}