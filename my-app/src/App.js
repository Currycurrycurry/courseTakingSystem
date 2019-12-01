import React,{Component} from 'react';
// import logo from './logo.svg';
import './App.css';
import axios from 'axios';

axios.default.withCredentials = true;
axios.defaults.headers.post['Content-type'] = 'application/json';
const server = 'http://127.0.0.1:8000/selectCourse';


// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

class App extends Component{
  constructor(props){
    super(props);
    this.state = {
      classroom_no:"",
      capacity:0
    }
    this.change = this.change.bind(this)
    this.write = this.write.bind(this)
    this.read = this.read.bind(this)
  }

  change(key,e){
    this.setState({
      [key]:e.target.value
    });
  }

  async write(){
    let data = {...this.state};
    console.log(data);
    let res = await axios.post(`${server}/write/`,data);
    console.log(res);
  }

  async read(){
    let params = {
      classroom_no:'Z3309'
    }

    let res = await axios.get(`${server}/read/`,{params});
    console.log(res);
  }

  render() {
    return (
      <div className="App">
        <input onChange={(e) => (this.change('classroom_no',e))} />
        <br/>
        <input onChange={(e) => (this.change('capacity',e))} />
        <br/>
        <button onClick={this.write}>write</button>
        <button onClick={this.read}>read</button>
      </div>
    );
  }
}

export default App;
