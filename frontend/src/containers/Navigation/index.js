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
      hashtags: [],
      dates: [],
      startDate: new Date('Feburary 7, 2019')
    }
  }

  componentDidMount() {
    this.getDates();
  }

  handleItemClick = (e, { name }) => {
    this.setState({ activeItem: name })

    if (name === 'hashtags'){
      this.getHashtags()
    }
  }

  handleChangeDate = (date) => {
    this.setState({
      startDate: date
    });
    console.log("testing date", date)
  }

  getHashtags = () => {
    if (this.state.hashtags && this.state.hashtags.length !== 0) {
      return;
    }

    api.getHashtags()
      .then(response => {
        this.setState({ hashtags: response.data });
      });
  }

  getDates = () => {
    api.getDates()
      .then(response => {
        this.setState({ dates: response.data });
      });
  }

  getHashtagsDate = () => {
    const date = "1/16/16"; // as an example
    const data = {"date": date}

    api.postHashtagsDate(data)
      .then(response => {
        console.log(response.data);
      });
  }

  postPlots = () => {
    const data = {
      "year": "2016",
      "form": "hashtags",
      "value": "#fash",
    };

    api.postPlots(data)
      .then(response => {
        console.log(response.data);
      });
  }

  render() {
    console.log("navigation", this.props.selection)
    const {
      hashtags,
      dates,
      activeItem,
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
          {hashtags.map((hashtag, idx) => (
            <Button
              className="resultButton"
              key={idx} size='mini' inverted color='grey'
              onClick={this.postPlots}
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
        <div className="mainHeader" > 01/01/2016 - 02/07/2019</div> 
         
        <DatePicker
            selected={this.state.startDate}
            onChange={this.handleChangeDate}
            minDate={new Date('January 1, 2016')}
            maxDate={new Date('Feburary 7, 2019')}
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

