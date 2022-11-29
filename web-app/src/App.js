import React, { useEffect, useState} from 'react'
import api from './api/timestream'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [data, setData] = useState({})
  const options = [
    {value: '24h', text: '24h'},
    {value: '12h', text: '12h'},
    {value: '6h', text: '6h'},
    {value: '1h', text: '1h'},
    {value: '7d', text: '7d'},
  ];
  const [selectedTimerange, setSelectedTimerange] = useState(options[0].value);
  const fetchData = async (measure_name,timerange) => {
      const q = `SELECT * FROM izunuma.izunuma WHERE (measure_name='${measure_name}') AND time >= ago(${timerange}) ORDER BY time ASC`
      console.log(q)
      const res = await api.rawQuery(q);
      console.log(res);
      const chartData = res.Rows.map((d)=>({
        time: d.Data[2].ScalarValue.slice(0, -10),
        value: d.Data[3].ScalarValue,
      }))
      return chartData
  }

  useEffect(() => {
    const initiallize = async () => {
      await api.setConfiguration('ap-northeast-1', process.env.REACT_APP_AWS_ID, process.env.REACT_APP_AWS_SECRET)
    }
    initiallize()
  }, [])
  const data_name = [
    ['0001DO_1','data_0001DO_1'],
    ['0001DO_2','data_0001DO_2'],
    ['0001TEMP','data_0001TEMP'],
    ['0002DO_1','data_0002DO_1'],
    ['0002DO_2','data_0002DO_2'],
    ['0002TEMP','data_0002TEMP'],
    ['0003DO_1','data_0003DO_1'],
    ['0003DO_2','data_0003DO_2'],
    ['0003TEMP','data_0003TEMP'],]
  useEffect(() => {
    const fetch = async () => {
      data_name.map(async (d)=>{
        const res = await fetchData(d[0],selectedTimerange);
        setData((data) => ({ ...data, [d[1]]: res }));
      })
    }
    fetch()
  }, [selectedTimerange])


  const handleSelectChange = e => {
    console.log(e.target.value);
    setSelectedTimerange(e.target.value);
  };

  return (
    <div className="App">
      <select value={selectedTimerange} onChange={handleSelectChange} className="select">
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.text}
          </option>
        ))}
      </select>
      <h1>center</h1>
      <div>
        <LineChart width={1000} height={400}>
          <Line type="monotone" dataKey="value" data={data.data_0001DO_1} stroke="#8884d8"/>
          <Line type="monotone" dataKey="value" data={data.data_0001DO_2} stroke="#82ca9d"/>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
          <YAxis />
          <Tooltip />
        </LineChart>
      </div>
      <div>
        <LineChart width={1000} height={400} data={data.data_0001TEMP}>
          <Line type="monotone" dataKey="value"  stroke="#8884d8"/>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
          <YAxis />
          <Tooltip />
        </LineChart>
      </div>
      <h1>west</h1>
      <div>
        <LineChart width={1000} height={400}>
          <Line type="monotone" dataKey="value" data={data.data_0002DO_1} stroke="#8884d8"/>
          <Line type="monotone" dataKey="value" data={data.data_0002DO_2} stroke="#82ca9d"/>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
          <YAxis />
          <Tooltip />
        </LineChart>
      </div>
      <div>
        <LineChart width={1000} height={400} data={data.data_0002TEMP}>
          <Line type="monotone" dataKey="value"  stroke="#8884d8"/>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
          <YAxis />
          <Tooltip />
        </LineChart>
      </div>
      <h1>east</h1>
      <div>
        <LineChart width={1000} height={400}>
          <Line type="monotone" dataKey="value" data={data.data_0003DO_1} stroke="#8884d8"/>
          <Line type="monotone" dataKey="value" data={data.data_0003DO_2} stroke="#82ca9d"/>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
          <YAxis />
          <Tooltip />
        </LineChart>
      </div>
      <div>
        <LineChart width={1000} height={400} data={data.data_0003TEMP}>
          <Line type="monotone" dataKey="value"  stroke="#8884d8"/>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
          <YAxis />
          <Tooltip />
        </LineChart>
      </div>
    </div>
  );
}

export default App;
