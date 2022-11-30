import React, { useEffect, useState} from 'react'
import api from './api/timestream'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import moment from 'moment'
import { CSVLink } from "react-csv";

function App() {
  const [data, setData] = useState({
    data_0001DO_1:[],
    data_0001DO_2:[],
    data_0001TEMP:[],
    data_0002DO_1:[],
    data_0002DO_2:[],
    data_0002TEMP:[],
    data_0003DO_1:[],
    data_0003DO_2:[],
    data_0003TEMP:[],
  })
  const [haveData, setHaveData] = useState(false)
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
        time: moment(d.Data[2].ScalarValue.slice(0, -10),"YYYY-MM-DD HH:mm:ss").valueOf(),
        value: d.Data[3].ScalarValue,
      }))
      return chartData
  }

  useEffect(() => {
    const initiallize = async () => {
      console.log(process.env.REACT_APP_AWS_ID);
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
    <div className="">
      <div class="navbar bg-primary">
        <div class="md:navbar-start">
        </div>
        <div class="navbar-start md:navbar-center text-primary-content">
          <a class="normal-case md:text-3xl text-2xl ml-2 md:mx-auto">IZUNUMA</a>
        </div>
        <div class="navbar-end">
        <div class="dropdown dropdown-end mr-2">
          <label tabindex="0" class="btn btn-accent">
            <p>export</p>
          </label>
          <div tabindex="0" class="mt-3 card card-compact dropdown-content w-52 bg-base-100 shadow">
            <div class="card-body">
              <CSVLink data={data.data_0001DO_1} filename={"center_DO_1.csv"}>center DO 1</CSVLink>
              <CSVLink data={data.data_0001DO_2} filename={"center_DO_2.csv"}>center DO 2</CSVLink>
              <CSVLink data={data.data_0001TEMP} filename={"center_TEMP.csv"}>center TEMP</CSVLink>
              <CSVLink data={data.data_0002DO_1} filename={"west_DO_1.csv"}>west DO 1</CSVLink>
              <CSVLink data={data.data_0002DO_2} filename={"west_DO_2.csv"}>west DO 2</CSVLink>
              <CSVLink data={data.data_0002TEMP} filename={"west_TEMP.csv"}>west TEMP</CSVLink>
              <CSVLink data={data.data_0003DO_1} filename={"east_DO_1.csv"}>east DO 1</CSVLink>
              <CSVLink data={data.data_0003DO_2} filename={"east_DO_2.csv"}>east DO 2</CSVLink>
              <CSVLink data={data.data_0003TEMP} filename={"east_TEMP.csv"}>east TEMP</CSVLink>
            </div>
          </div>
        </div>

              <select value={selectedTimerange} onChange={handleSelectChange} className="select">
                {options.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.text}
                  </option>
                ))}
              </select>


        </div>
      </div>

      <div className="text-center content-center">

        <div class="card w-11/12 md:w-5/6 bg-base-100 shadow-xl mx-auto mt-5">
          <div class="card-body px-1 md:px-10">
            <h2 class="card-title text-5xl">center</h2>
            <p>DO</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} className="mx-auto">
                <Line type="monotone" dataKey="value" data={data.data_0001DO_1} stroke="#8884d8"/>
                <Line type="monotone" dataKey="value" data={data.data_0001DO_2} stroke="#82ca9d"/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
              </LineChart>
            </ResponsiveContainer>
            {data.data_0001DO_1.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 1)</span>
              </div>
            </div>
            :<></>}
            {data.data_0001DO_2.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 2)</span>
              </div>
            </div>
            :<></>}
            <p>TEMP</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} data={data.data_0001TEMP} className="mx-auto">
                <Line type="monotone" dataKey="value"  stroke="#8884d8"/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
              </LineChart>
            </ResponsiveContainer>
            {data.data_0001TEMP.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (TEMP)</span>
              </div>
            </div>
            :<></>}
          </div>
        </div>

        <div class="card w-11/12 md:w-5/6 bg-base-100 shadow-xl mx-auto mt-5">
          <div class="card-body px-1 md:px-10">
            <h2 class="card-title text-5xl">west</h2>
            <p>DO</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} className="mx-auto">
                <Line type="monotone" dataKey="value" data={data.data_0002DO_1} stroke="#8884d8"/>
                <Line type="monotone" dataKey="value" data={data.data_0002DO_2} stroke="#82ca9d"/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
              </LineChart>
            </ResponsiveContainer>
            {data.data_0002DO_1.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 1)</span>
              </div>
            </div>
            :<></>}
            {data.data_0002DO_2.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 2)</span>
              </div>
            </div>
            :<></>}
            <p>TEMP</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} data={data.data_0002TEMP} className="mx-auto">
                <Line type="monotone" dataKey="value"  stroke="#8884d8"/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
              </LineChart>
            </ResponsiveContainer>
            {data.data_0002TEMP.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (TEMP)</span>
              </div>
            </div>
            :<></>}
          </div>
        </div>

        <div class="card w-11/12 md:w-5/6 bg-base-100 shadow-xl mx-auto mt-5">
          <div class="card-body px-1 md:px-10">
            <h2 class="card-title text-5xl">east</h2>
            <p>DO</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} className="mx-auto">
                <Line type="monotone" dataKey="value" data={data.data_0003DO_1} stroke="#8884d8"/>
                <Line type="monotone" dataKey="value" data={data.data_0003DO_2} stroke="#82ca9d"/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
              </LineChart>
            </ResponsiveContainer>
            {data.data_0003DO_1.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 1)</span>
              </div>
            </div>
            :<></>}
            {data.data_0003DO_2.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 2)</span>
              </div>
            </div>
            :<></>}
            <p>TEMP</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} data={data.data_0003TEMP} className="mx-auto">
                <Line type="monotone" dataKey="value"  stroke="#8884d8"/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
              </LineChart>
            </ResponsiveContainer>
            {data.data_0003TEMP.length==0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found</span>
              </div>
            </div>
            :<></>}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
