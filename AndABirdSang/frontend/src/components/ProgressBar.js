import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { LinearProgress, LinearProgressWithLabel, CircularProgress } from "@material-ui/core";

export default class ProgressBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            progress: 0,

        };
        this.taskID = this.props.match.params.taskID;
        this.getProgress = this.getProgress.bind(this);
        this.getProgress();

    }
    
    getProgress() {

        fetch(`/twitter/get-progress/${this.taskID}`)
        .then((response) => response.json())
        .then((data) => {
            this.setState({ progress: data.progress})
        })
    }


    render() {
        /*
        this.getProgress();
        
        if (this.state.progress == 0) {
            return (<Grid><CircularProgress color="secondary" /></Grid>);
        }
        
        if (this.state.progress != 0 && this.state.progress != 100) {
            return (
            <Grid>
                <h1>{this.state.progress}</h1>
                <LinearProgressWithLabel value={this.state.progress} />
            </Grid> )
            
        }

        if (this.state.progress == 100) {
            return (<h1>Success</h1>);
        } */
        
        return (
            <Grid>
<               Grid>
                    {this.getProgress()}
                    <Typography>{this.state.progress}</Typography>
                    {this.state.progress == 0 ? <Grid><CircularProgress color="secondary" /></Grid> : <Grid><LinearProgress variant="determinate" value={this.state.progress} /></Grid>}
                </Grid>
            </Grid>
            
        )
    };

}
