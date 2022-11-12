import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core";
import FormControl from "@material-ui/core/FormControl";

export default class CreatePlaylist extends Component {
    constructor(props) {
        super(props);
        this.state = {
            

        };

        

    }

    handleCreatePlaylistButtonPressed() {
        fetch("/spotify/create-playlist")
        .then((response) => response.json())
        .then((data) => {
            window.location.replace(data.url);
        })
        
    }

    render() {
        
        return (
            <Grid container spacing={1}>
                
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="primary" onClick={this.handleCreatePlaylistButtonPressed}>
                        Create Playlist
                    </Button>
                        
                </Grid>
                
            </Grid>
        
        )
    };
}