import React, {useState, useEffect} from 'react'

function App() {
  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/test").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, []) // empty list means no dependencies, stops infinite rendering loop

  return (
    <div>
      {(typeof(data.testy) === "undefined") ? (
        <p>Loading...</p>
      ) : (
        data.testy.map((value, index) => (
          <p key = {index}>{value}</p>
        ))
      )}
    </div>
  )
}

export default App