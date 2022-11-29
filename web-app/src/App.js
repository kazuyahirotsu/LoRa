import React, { useEffect, useState } from 'react'
import api from './api/timestream'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [data, setData] = useState()
  useEffect(() => {
    const initiallize = async () => {
      await api.setConfiguration('ap-northeast-1', process.env.REACT_APP_AWS_ID, process.env.REACT_APP_AWS_SECRET)

      const q = `SELECT * FROM izunuma.izunuma WHERE measure_name='0001DO_1' AND time >= ago(24h)`
      const res = await api.rawQuery(q);
      const chartData = res.Rows.map((d)=>({
        time: d.Data[2].ScalarValue.slice(0, -10),
        value: d.Data[3].ScalarValue
      }))
      setData(chartData);
      console.log(chartData);
    }
    initiallize()
  }, [])

  return (
    <div className="App">
      <h1>0001 DO 1</h1>
      <LineChart width={1000} height={400} data={data}>
        <Line type="monotone" dataKey="value" stroke="#8884d8"/>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" angle={-45} textAnchor="end" tick={{ fontSize: '.7rem' }} height={100}/>
        <YAxis />
        <Tooltip />
      </LineChart>
    </div>
  );
}

export default App;
