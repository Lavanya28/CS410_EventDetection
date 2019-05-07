import React, { Component } from 'react';

class Navigation extends Component {
  render() {
    return (
      <div
        className="Navigation"
      >
        <form>
          <button name="top" value="Top trending hashtags">Top trending hashtags</button>
          <button name="top" value="Top trending words">Top trending words</button>
          <button name="top" value="Top trending word-pairs">Top trending word-pairs</button>
          <select value="Select a Year">
            <option id="2016" value="2016">2016</option>
            <option id="2017" value="2017">2017</option>
            <option id="2018" value="2018">2018</option>
            <option id="2019" value="2019">2019</option>
          </select>
        </form>
      </div>
    );
  }
}

export default Navigation;

