### Generic Variables
    variable "region" {
    type = string
    default = "eu-central-1"
    }

    variable "name" {
        type = string
        default = "test-frontend-1-tf"
    }

    variable "template" {
    type    = string
    default = "containarized_frontend"
    }

    variable "application" {
    type    = string
    default = ""
    }

    variable "purpose" {
    type    = string
    default = "setting up frontend services"
    }

    variable "created-on" {
    type    = string
    default = "25_April_2021"
    }