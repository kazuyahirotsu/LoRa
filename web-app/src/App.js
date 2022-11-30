import React, { useEffect, useState} from 'react'
import api from './api/timestream'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import moment from 'moment'
import { CSVLink } from "react-csv";
import { CiExport } from "react-icons/ci";

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
  const [latestData, setLatestData] = useState({
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
  const options = [
    {value: '24h', text: '24h'},
    {value: '12h', text: '12h'},
    {value: '6h', text: '6h'},
    {value: '1h', text: '1h'},
    {value: '7d', text: '7d'},
    {value: '14d', text: '14d'},
  ];
  const [selectedTimerange, setSelectedTimerange] = useState(options[0].value);
  const [timerangeStart, setTimerangeStart] = useState(moment(new Date()).subtract(24,'hours').format("YYYY-MM-DD HH:mm:ss"));
  const [timerangeEnd, setTimerangeEnd] = useState(moment(new Date()).format("YYYY-MM-DD HH:mm:ss"));
  const [textInputTimerangeStart, setTextInputTimerangeStart] = useState(moment(new Date()).subtract(24,'hours').format("YYYY-MM-DD HH:mm:ss"));
  const [textInputTimerangeEnd, setTextInputTimerangeEnd] = useState(moment(new Date()).format("YYYY-MM-DD HH:mm:ss"));

  const fetchData = async (measure_name,timerangeStart,timerangeEnd) => {
      const q = `SELECT * FROM izunuma.izunuma WHERE (measure_name='${measure_name}') AND time BETWEEN '${moment(timerangeStart).subtract(9,'hours').format("YYYY-MM-DD HH:mm:ss")}' AND '${moment(timerangeEnd).subtract(9,'hours').format("YYYY-MM-DD HH:mm:ss")}' ORDER BY time ASC`
      const res = await api.rawQuery(q);
      const chartData = res.Rows.map((d)=>({
        time: moment(d.Data[2].ScalarValue.slice(0, -10),"YYYY-MM-DD HH:mm:ss").add(9, 'hours').valueOf(),
        value: d.Data[3].ScalarValue,
      }))
      return chartData
  }
  const fetchLatestData = async (measure_name) => {
    const q = `SELECT * FROM izunuma.izunuma WHERE (measure_name='${measure_name}')  ORDER BY time DESC LIMIT 1`
    const res = await api.rawQuery(q);
    const chartData = res.Rows.map((d)=>({
      time: moment(d.Data[2].ScalarValue.slice(0, -10),"YYYY-MM-DD HH:mm:ss").add(9, 'hours').valueOf(),
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
    const fetchLatest = async () => {
      data_name.map(async (d)=>{
        const res = await fetchLatestData(d[0]);
        setLatestData((data) => ({ ...data, [d[1]]: res }));
      })
    }
    fetchLatest()
    const fetch = async () => {
      data_name.map(async (d)=>{
        const res = await fetchData(d[0], timerangeStart, timerangeEnd);
        setData((data) => ({ ...data, [d[1]]: res }));
      })
    }
    fetch()
  }, [timerangeStart,timerangeEnd])

  useEffect(() => {
    if(selectedTimerange[selectedTimerange.length-1]==='h'){
      setTimerangeStart(moment(new Date()).subtract(selectedTimerange.substr(0, selectedTimerange.indexOf('h')),'hours').format("YYYY-MM-DD HH:mm:ss"));
      setTextInputTimerangeStart(moment(new Date()).subtract(selectedTimerange.substr(0, selectedTimerange.indexOf('h')),'hours').format("YYYY-MM-DD HH:mm:ss"));
    }else if(selectedTimerange[selectedTimerange.length-1]==='d'){
      setTimerangeStart(moment(new Date()).subtract(selectedTimerange.substr(0, selectedTimerange.indexOf('d')),'days').format("YYYY-MM-DD HH:mm:ss"));
      setTextInputTimerangeStart(moment(new Date()).subtract(selectedTimerange.substr(0, selectedTimerange.indexOf('d')),'days').format("YYYY-MM-DD HH:mm:ss"));
    }
    setTimerangeEnd(moment(new Date()).format("YYYY-MM-DD HH:mm:ss"));
    setTextInputTimerangeEnd(moment(new Date()).format("YYYY-MM-DD HH:mm:ss"));
  }, [selectedTimerange])

  const handleSelectChange = e => {
    setSelectedTimerange(e.target.value);
  };
  const handleChangeTextInputTimerangeStart = e => {
    setTextInputTimerangeStart(e.target.value);
  };
  const handleChangeTextInputTimerangeEnd = e => {
    setTextInputTimerangeEnd(e.target.value);
  };
  const onSubmitTimerange = e => {
    setTimerangeStart(textInputTimerangeStart);
    setTimerangeEnd(textInputTimerangeEnd);
  };

  return (
    <div>
      <div class="navbar bg-primary shadow-xl">
        <div class="md:navbar-start">
        </div>
        <div class="navbar-start md:navbar-center text-primary-content">
          <a class="normal-case md:text-3xl text-2xl ml-2 md:mx-auto">IZUNUMA</a>
        </div>
        <div class="navbar-end">
          <select value={selectedTimerange} onChange={handleSelectChange} className="select mr-2">
            {options.map(option => (
              <option key={option.value} value={option.value}>
                {option.text}
              </option>
            ))}
          </select>
          <div class="dropdown dropdown-end mr-2">
            <label tabindex="0" class="btn">
              <p>custom range</p>
            </label>
            <div tabindex="0" class="mt-3 card card-compact dropdown-content w-52 bg-base-100 shadow">
              <div class="card-body text-center">
              <p className='text-accent'>YYYY-MM-DD HH:mm:ss</p>
              <input className='input' type="text" value={textInputTimerangeStart} onChange={handleChangeTextInputTimerangeStart} />
              <input className='input' type="text" value={textInputTimerangeEnd} onChange={handleChangeTextInputTimerangeEnd} />
              <button className="btn" onClick={onSubmitTimerange}>
                show
              </button>
              </div>
            </div>
          </div>
          <div class="dropdown dropdown-end mr-2">
            <label tabindex="0" class="btn btn-accent">
              <CiExport />
            </label>
            <div tabindex="0" class="mt-3 card card-compact dropdown-content w-52 bg-base-100 shadow">
              <div class="card-body">
                <CSVLink data={data.data_0001DO_1} filename={"center_DO_1.csv"}><p className='text-base'>center DO 1</p></CSVLink>
                <CSVLink data={data.data_0001DO_2} filename={"center_DO_2.csv"}><p className='text-base'>center DO 2</p></CSVLink>
                <CSVLink data={data.data_0001TEMP} filename={"center_TEMP.csv"}><p className='text-base'>center TEMP</p></CSVLink>
                <CSVLink data={data.data_0002DO_1} filename={"west_DO_1.csv"}><p className='text-base'>west DO 1</p></CSVLink>
                <CSVLink data={data.data_0002DO_2} filename={"west_DO_2.csv"}><p className='text-base'>west DO 2</p></CSVLink>
                <CSVLink data={data.data_0002TEMP} filename={"west_TEMP.csv"}><p className='text-base'>west TEMP</p></CSVLink>
                <CSVLink data={data.data_0003DO_1} filename={"east_DO_1.csv"}><p className='text-base'>east DO 1</p></CSVLink>
                <CSVLink data={data.data_0003DO_2} filename={"east_DO_2.csv"}><p className='text-base'>east DO 2</p></CSVLink>
                <CSVLink data={data.data_0003TEMP} filename={"east_TEMP.csv"}><p className='text-base'>east TEMP</p></CSVLink>
              </div>
            </div>
          </div>
      </div>
    </div>

      <div className="text-center content-center">
        <div class="card w-11/12 md:w-5/6 bg-base-100 shadow-xl mx-auto mt-5">
          <div class="card-body px-1 md:px-10">
            <h2 class="card-title text-5xl">center</h2>
            <p className='text-xl font-semibold'>latest data</p>
            <div class="stats shadow mb-3">
              {latestData.data_0001DO_1[latestData.data_0001DO_1.length-1]?
              <div class="stat">
                <div class="stat-title">DO 1</div>
                <div class="stat-value text-primary">{latestData.data_0001DO_1[latestData.data_0001DO_1.length-1].value}mg/L</div>
                <div class="stat-desc">{moment(latestData.data_0001DO_1[latestData.data_0001DO_1.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}

              {latestData.data_0001DO_2[latestData.data_0001DO_2.length-1]?
              <div class="stat">
                <div class="stat-title">DO 2</div>
                <div class="stat-value text-primary">{latestData.data_0001DO_2[latestData.data_0001DO_2.length-1].value}mg/L</div>
                <div class="stat-desc">{moment(latestData.data_0001DO_2[latestData.data_0001DO_2.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}

              {latestData.data_0001TEMP[latestData.data_0001TEMP.length-1]?
              <div class="stat">
                <div class="stat-title">TEMP</div>
                <div class="stat-value text-primary">{latestData.data_0001TEMP[latestData.data_0001TEMP.length-1].value}°C</div>
                <div class="stat-desc">{moment(latestData.data_0001TEMP[latestData.data_0001TEMP.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}
            </div>
            <p className='text-xl font-semibold'>DO</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} className="mx-auto">
                <Line type="monotone" dataKey="value" data={data.data_0001DO_1} name="DO1" stroke="#8884d8" dot={false}/>
                <Line type="monotone" dataKey="value" data={data.data_0001DO_2} name="DO2" stroke="#82ca9d" dot={false}/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" interval="preserveStart" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip formatter={(value, name, props) => value+"mg/L"} labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
                <Legend />
              </LineChart>
            </ResponsiveContainer>
            {data.data_0001DO_1.length===0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 1)</span>
              </div>
            </div>
            :<></>}
            {data.data_0001DO_2.length===0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 2)</span>
              </div>
            </div>
            :<></>}
            <p className='text-xl font-semibold'>TEMP</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} data={data.data_0001TEMP} className="mx-auto">
                <Line type="monotone" dataKey="value" name="TEMP" stroke="#ffc658" dot={false}/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" interval="preserveStart" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip formatter={(value, name, props) => value+"°C"} labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
                <Legend />
              </LineChart>
            </ResponsiveContainer>
            {data.data_0001TEMP.length===0?
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
            <p className='text-xl font-semibold'>latest data</p>
            <div class="stats shadow">
              {latestData.data_0002DO_1[latestData.data_0002DO_1.length-1]?
              <div class="stat">
                <div class="stat-title">DO 1</div>
                <div class="stat-value text-primary">{latestData.data_0002DO_1[latestData.data_0002DO_1.length-1].value}mg/L</div>
                <div class="stat-desc">{moment(latestData.data_0002DO_1[latestData.data_0002DO_1.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}

              {latestData.data_0002DO_2[latestData.data_0002DO_2.length-1]?
              <div class="stat">
                <div class="stat-title">DO 2</div>
                <div class="stat-value text-primary">{latestData.data_0002DO_2[latestData.data_0002DO_2.length-1].value}mg/L</div>
                <div class="stat-desc">{moment(latestData.data_0002DO_2[latestData.data_0002DO_2.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}

              {latestData.data_0002TEMP[latestData.data_0002TEMP.length-1]?
              <div class="stat">
                <div class="stat-title">TEMP</div>
                <div class="stat-value text-primary">{latestData.data_0002TEMP[latestData.data_0002TEMP.length-1].value}°C</div>
                <div class="stat-desc">{moment(latestData.data_0002TEMP[latestData.data_0002TEMP.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}
            </div>
            <p className='text-xl font-semibold'>DO</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} className="mx-auto">
                <Line type="monotone" dataKey="value" data={data.data_0002DO_1} name="DO1" stroke="#8884d8" dot={false}/>
                <Line type="monotone" dataKey="value" data={data.data_0002DO_2} name="DO2" stroke="#82ca9d" dot={false}/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" interval="preserveStart" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip formatter={(value, name, props) => value+"mg/L"} labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
                <Legend />
              </LineChart>
            </ResponsiveContainer>
            {data.data_0002DO_1.length===0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 1)</span>
              </div>
            </div>
            :<></>}
            {data.data_0002DO_2.length===0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 2)</span>
              </div>
            </div>
            :<></>}
            <p className='text-xl font-semibold'>TEMP</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} data={data.data_0002TEMP} className="mx-auto">
                <Line type="monotone" dataKey="value" name="TEMP" stroke="#ffc658" dot={false}/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" interval="preserveStart" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip formatter={(value, name, props) => value+"°C"} labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
                <Legend />
              </LineChart>
            </ResponsiveContainer>
            {data.data_0002TEMP.length===0?
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
            <p className='text-xl font-semibold'>latest data</p>
            <div class="stats shadow">
              {latestData.data_0003DO_1[latestData.data_0003DO_1.length-1]?
              <div class="stat">
                <div class="stat-title">DO 1</div>
                <div class="stat-value text-primary">{latestData.data_0003DO_1[latestData.data_0003DO_1.length-1].value}mg/L</div>
                <div class="stat-desc">{moment(latestData.data_0003DO_1[latestData.data_0003DO_1.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}

              {latestData.data_0003DO_2[latestData.data_0003DO_2.length-1]?
              <div class="stat">
                <div class="stat-title">DO 2</div>
                <div class="stat-value text-primary">{latestData.data_0003DO_2[latestData.data_0003DO_2.length-1].value}mg/L</div>
                <div class="stat-desc">{moment(latestData.data_0003DO_2[latestData.data_0003DO_2.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}

              {latestData.data_0003TEMP[latestData.data_0003TEMP.length-1]?
              <div class="stat">
                <div class="stat-title">TEMP</div>
                <div class="stat-value text-primary">{latestData.data_0003TEMP[latestData.data_0003TEMP.length-1].value}°C</div>
                <div class="stat-desc">{moment(latestData.data_0003TEMP[latestData.data_0003TEMP.length-1].time).format("YYYY-MM-DD HH:mm:ss")}</div>
              </div>
              :<></>}
            </div>
            <p className='text-xl font-semibold'>DO</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} className="mx-auto">
                <Line type="monotone" dataKey="value" data={data.data_0003DO_1} name="DO1" stroke="#8884d8" dot={false}/>
                <Line type="monotone" dataKey="value" data={data.data_0003DO_2} name="DO2" stroke="#82ca9d" dot={false}/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" interval="preserveStart" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip formatter={(value, name, props) => value+"mg/L"} labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
                <Legend />
              </LineChart>
            </ResponsiveContainer>
            {data.data_0003DO_1.length===0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 1)</span>
              </div>
            </div>
            :<></>}
            {data.data_0003DO_2.length===0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (DO 2)</span>
              </div>
            </div>
            :<></>}
            <p className='text-xl font-semibold'>TEMP</p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart width={1000} height={400} data={data.data_0003TEMP} className="mx-auto">
                <Line type="monotone" dataKey="value" name="TEMP" stroke="#ffc658" dot={false}/>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" type="number" interval="preserveStart" tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM-DD HH:mm:ss")} domain={['auto', 'auto']} scale="time"  allowDuplicatedCategory={false} angle={-45} textAnchor="end" tick={{ fontSize: '.7rem', color: 'white'}} height={100} className="text-white"/>
                <YAxis type="number" domain={[0,20]}/>
                <Tooltip formatter={(value, name, props) => value+"°C"} labelFormatter={(label) => moment(label).format("YYYY-MM-DD HH:mm:ss")}/>
                <Legend />
              </LineChart>
            </ResponsiveContainer>
            {data.data_0003TEMP.length===0?
            <div class="alert alert-error shadow-lg">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>No data found (TEMP)</span>
              </div>
            </div>
            :<></>}
          </div>
        </div>
      </div>

      <footer className="footer p-10 bg-neutral text-neutral-content mt-5 text-center content-center">
        <a href="https://github.com/kazuyahirotsu/LoRa" target="_blank" className='mx-auto'>github repo</a>
      </footer>
    </div>
  );
}

export default App;