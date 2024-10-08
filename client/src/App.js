import React, {useState, useEffect} from 'react'

function App() {
  const [linkType, setLinkType] = useState("chapter")
  const [link, setLink] = useState("")
  const [pathway, setPathway] = useState("")
  const [chapterStart, setChapterStart] = useState("")
  const [chapterEnd, setChapterEnd] = useState("")
  const [result, setResult] = useState("Nothing Yet")

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
    console.log(data)
    setResult("Loading...")
    fetch("/read_link", { // has to have fetch and then?
      method: "POST", // what does method and headers do?
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    })
    .then((res) => res.json())
    .then((res) => {
      console.log(res)
      if (res.status) {
        setResult(res.status)
      }
      if (res.error) {
        setResult(res.error)
      }
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
          placeholder = "ex: C:\Users\justi\Downloads"
          required
        />

        <br></br><br></br>

        <label htmlFor = "start-input">(Optional For Series) Chapter Start Name: </label>
        <input
          id = "start-input"
          type = "text"
          name = "chapter-start"
          onChange = {handleStartChange}
          value = {chapterStart}
        />

        <br></br><br></br>

        <label htmlFor = "end-input">(Optional For Series) Chapter End Name: </label>
        <input
          id = "end-input"
          type = "text"
          name = "chapter-end"
          onChange = {handleEndChange}
          value = {chapterEnd}
        />

        <br></br><br></br>

        <button type = "submit">Read Link</button>
      </form>

      <p>{result}</p>
    </>
  )
}

export default App