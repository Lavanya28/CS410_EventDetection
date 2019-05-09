import React, { Component } from 'react';
import { Segment, Header, Dropdown, Menu, Divider,Button } from 'semantic-ui-react'
import DatePicker from "react-datepicker";
import api from '../../api';
import { yearOptions } from './options';
import './styles.scss';
import './date-picker.scss';

class Navigation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      spikeWords: [],
      dates: [],
      year: 2016,
      startDate: new Date('February 7, 2019'),
      activeItem: "",
      eventHastags:[]
    }
  }

  componentDidMount() {
    this.getDates();
  }

  handleItemClick = (e, { name }) => {
    this.setState({ activeItem: name })
    this.getspikeWords(name,this.state.year)
  }

  handleDropdownDateChange = (e,{ value })=>{
    this.setState({year:value})
    if (this.state.activeItem !== ''){
      this.getspikeWords(this.state.activeItem,value)
    }
   
  }

  handleChangeDate = (date) => {
    this.setState({
      startDate: date
    });

    console.log("testing date", date)
    var n = date.toLocaleDateString();
    this.getHashtagsDate(n)

  }

  getspikeWords = (name, year) => {
    let post_request = {}
    post_request = {
      word_type:name,
      time_frame:year
    }

    console.log(post_request)
    api.postSpikeDetection(post_request)
      .then(response => {
        this.setState({ spikeWords: response.data });
      });
  }

  getDates = () => {
    api.getDates()
      .then(response => {
        this.setState({ dates: response.data });
      });
  }

  getHashtagsDate = (date) => {
    // const date = "1/16/16"; // as an example
    const {
      changeHashtags,
    } = this.props;

    const data = {"date": date}

    api.postHashtagsDate(data)
      .then(response => {
        changeHashtags(response.data);
      });
  }

  postPlots = (value) => {
    const {
      year,
      activeItem,
    } = this.state;
    const {
      changePlot,
    } = this.props;

    const data = {
      "year": year,
      "form": activeItem,
      "value": value,
    };

    api.postPlots(data)
      .then(response => {
        changePlot(response.path, response.title);
      });
  }

  render() {
    const {
      spikeWords,
      dates,
      activeItem,
      year
    } = this.state;
    const { selection } = this.props;

    const spikeInfo = (
      <div>
        <React.Fragment>
        <Header className="mainHeader" size= "small">Select Time Frame</Header>            
             <Dropdown className="year"
               placeholder='Choose Year'
               // selection
               openOnFocus
               inline
               value={year}
               onChange={this.handleDropdownDateChange}
               options={yearOptions}
             />
        </React.Fragment>
        <Header  className="mainHeader"  size= "small">Top 50 Trending</Header>
        <Menu className="contentMenu" widths={3} compact size='mini'>
          <Menu.Item name='unigrams' 
                     active={activeItem === 'unigrams'} 
                     onClick={this.handleItemClick} 
          />
          <Menu.Item name='hashtags' 
                     active={activeItem === 'hashtags'} 
                     onClick={this.handleItemClick} 
          />
          <Menu.Item name='wordpairs' 
                     active={activeItem === 'wordpairs'} 
                     onClick={this.handleItemClick} />
        </Menu>
        <Divider />
        <div className="Generated">
        <Header size= "small">Generated results: </Header>
        <div className="Navigation-options">
          {spikeWords.map((hashtag, idx) => (
            <Button
              className="resultButton"
              key={idx} size='mini' inverted color='grey'
              onClick={() => this.postPlots(hashtag[0])}
            >
              {hashtag[0]}
            </Button>
          ))}
        </div>
        </div>
      </div>
    );

    const eventInfo = (
      <div>
        <Header className="mainHeader" size= "small">Choose a date between</Header>
        <div className="mainHeader" > 01/16/2016 - 02/07/2019</div> 
         
        <DatePicker
            selected={this.state.startDate}
            onChange={this.handleChangeDate}
            minDate={new Date('January 16, 2016')}
            maxDate={new Date('February 7, 2019')}
            showMonthDropdown
        />
      </div>
    );

    let navigationInfo = spikeInfo

    if(selection === 'events'){
      navigationInfo = eventInfo;
    }else if(selection === 'topics'){
      navigationInfo = (
        <div>
          topics
        </div>
      )
    }else{
      navigationInfo = spikeInfo;
    }

    return (
      <Segment raised className="Navigation">
        {navigationInfo}
      </Segment>
    );
  }
}

export default Navigation;

