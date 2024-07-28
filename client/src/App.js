import React, {useState, useEffect} from 'react'

function App() {
  const [linkType, setLinkType] = useState("chapter")
  const [link, setLink] = useState("")
  const [pathway, setPathway] = useState("C:\\Users\\Webnovel Chapters\\")
  const [chapterStart, setChapterStart] = useState("")
  const [chapterEnd, setChapterEnd] = useState("")
  const [result, setResult] = useState("nothing yet")

  // const [data, setData] = useState([{}])
  // useEffect(() => {
  //   fetch("/test").then(
  //     res => res.json()
  //   ).then(
  //     data => {
  //       setData(data)
  //       console.log(data)
  //     }
  //   )
  // }, []) // empty list means no dependencies, stops infinite rendering loop

  // WHAT DOES USEEFFECT DO?

  function handleSubmit(event) {
    event.preventDefault();
    const data = {
      linkType: linkType,
      link: link,
      pathway: pathway,
      chapterStart: chapterStart,
      chapterEnd: chapterEnd
    }
    // console.log(data)
    fetch("/test", { // has to have fetch and then?
      method: "POST", // what does method and headers do?
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    })
    .then((res) => res.json())
    .then((res) => {
      console.log(res)
      setResult(res.status)
    })
  }

  function handleLinkTypeChange(event) {
    setLinkType(event.target.value) // change the state var into the value property of whatever called the event
  }

  function handleLinkChange(event) {
    setLink(event.target.value)
  }

  function handlePathwayChange(event) {
    setPathway(event.target.value)
  }

  function handleStartChange(event) {
    setChapterStart(event.target.value)
  }

  function handleEndChange(event) {
    setChapterEnd(event.target.value)
  }

  return (
    // <div>
    //   {(typeof(data.testy) === "undefined") ? (
    //     <p>Loading...</p>
    //   ) : (
    //     data.testy.map((value, index) => (
    //       <p key = {index}>{value}</p>
    //     ))
    //   )}
    // </div>

    <>
      <form onSubmit = {handleSubmit}>
        <label htmlFor = "link-type-select">Select Link Type: </label>
        <select id = "link-type-select" name = "link-type" onChange = {handleLinkTypeChange} required>
          <option value = "chapter">Chapter</option>
          <option value = "series">Series</option>
        </select>

        <br></br><br></br>

        <label htmlFor = "link-input">Enter Chapter or Series Link: </label>
        <input
          id = "link-input"
          type = "text"
          name = "link"
          onChange = {handleLinkChange}
          value = {link}
          required
        />

        <br></br><br></br>

        <label htmlFor = "pathway-input">Enter Download Pathway: </label>
        <input
          id = "pathway-input"
          type = "text"
          name = "pathway"
          onChange = {handlePathwayChange}
          value = {pathway}
          required
        />

        <br></br><br></br>

        <label htmlFor = "start-input">(Optional) Enter Chapter Start: </label>
        <input
          id = "start-input"
          type = "text"
          name = "chapter-start"
          onChange = {handleStartChange}
          value = {chapterStart}
        />

        <br></br><br></br>

        <label htmlFor = "end-input">(Optional) Enter Chapter End: </label>
        <input
          id = "end-input"
          type = "text"
          name = "chapter-end"
          onChange = {handleEndChange}
          value = {chapterEnd}
        />

        <br></br><br></br>

        <button type = "submit">Submit Button</button>
      </form>

      <p>{result}</p>
    </>
  )
}

export default App