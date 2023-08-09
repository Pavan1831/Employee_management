*** Settings ***
Library     SeleniumLibrary
Library    RequestsLibrary
Test Setup       Open Browser    ${base_url}    chrome
Test Teardown    Close Browser


*** Variables ***
${base_url}     http://127.0.0.1:5000/
${VALID_USERNAME}    pavan
${VALID_PASSWORD}    pavan
${INVALID_USERNAME}    invaliduser
${INVALID_PASSWORD}    invalidpassword

*** Test Cases ***
Login and Logout Test
    [Documentation]    Verify successful login and logout
    Create Session  DummyAPI    ${base_url}
    ${response}     GET On Session  DummyAPI    /login
    Input Text    username    ${VALID_USERNAME}
    Input Text    password    ${VALID_PASSWORD}
    Click Button    Login
    Wait Until Element Is Visible    //h1[text()='Employee Management']
    Click Link    Logout
    Location Should Be    http://127.0.0.1:5000/login
    Log To Console    Login and Logout Successfull
    Log To Console    --------------------------------------

Login Page Elements Test
    [Documentation]    Verify the presence of login page elements
    Create Session  DummyAPI    ${base_url}
    ${response}     GET On Session  DummyAPI    /login
    Page Should Contain Element    //input[@name='username']
    Page Should Contain Element    //input[@name='password']
    Page Should Contain Element    //input[@type='submit']
    Page Should Contain Element    //a[text()='Sign up']
    Log To Console    Login page elements verified
    Log To Console    --------------------------------------

Valid Login Test
    [Documentation]    Verify successful login with valid credentials
    Create Session  DummyAPI    ${base_url}
    ${response}     GET On Session  DummyAPI    /login
    Should Be Equal As Strings    ${response.status_code}    200
    Input Text    //input[@name='username']    ${VALID_USERNAME}
    Input Text    //input[@name='password']    ${VALID_PASSWORD}
    Click Button    //input[@type='submit']
    Wait Until Element Is Visible    //h1[text()='Employee Management']
    Log To Console    Login Successfull
    Page Should Not Contain    Invalid username or password. Please try again.
    Log To Console    --------------------------------------

Invalid Credentials Test
    [Documentation]    Verify error message for invalid login credentials
    Create Session  DummyAPI    ${base_url}
    ${response}     GET On Session  DummyAPI    /login
    Input Text   //input[@name='username']     ${INVALID_USERNAME}
    Input Text    //input[@name='password']    ${INVALID_PASSWORD}
    Click Button    //input[@type='submit']
    Wait Until Element Is Visible    //p[text()='Invalid username or password. Please try again.']
    Log To Console    Invalid credentials
    Log To Console    ----------------------------------------

Empty Fields Test
    [Documentation]    Verify error message when attempting to login with empty fields
    Create Session  DummyAPI    ${base_url}
    ${response}     GET On Session  DummyAPI    /login
    Click Button    //input[@type='submit']
    Wait Until Element Is Visible    //p[text()='Invalid username or password. Please try again.']
    Log To Console    Enter credentials
    Log To Console    ----------------------------------------

Sign Up Link Test
    [Documentation]    Verify redirection to signup page when clicking the sign-up link
    Create Session  DummyAPI    ${base_url}
    ${response}     GET On Session  DummyAPI    /login
    Click Link    //a[text()='Sign up']
    Location Should Be    http://127.0.0.1:5000/signup
    Log To Console    Redirection to Signup page
    Log To Console    --------------------------------------








