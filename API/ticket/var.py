def ticket_generator(from_: str, to: str, flight: str,
                     date: str, time: str, gate: str,
                     seat: str, airline_logo: str,
                     airline_name: str, fullname: str):
    return f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Untitled Page</title>
    <meta
      name="generator"
      content="WYSIWYG Web Builder 19 Trial Version - https://www.wysiwygwebbuilder.com" />
    <link href="Untitled1.css" rel="stylesheet" />
    <link href="index.css" rel="stylesheet" />
  </head>
  <body>
    <div
      id="Html1"
      style="
        position: absolute;
        left: 0px;
        top: 0px;
        width: 991px;
        height: 386px;
        z-index: 0;
        background-color: #54A6B2;
      "></div>
    <hr
      id="HorizontalLine1"
      style="
        position: absolute;
        left: 0px;
        top: 67px;
        width: 692px;
        z-index: 1;
      " />
    <div
      id="wb_Text1"
      style="
        position: absolute;
        left: 38px;
        top: 174px;
        width: 175px;
        height: 30px;
        z-index: 2;
      ">
      <p>Flight: {flight}</p>
    </div>
    <div
      id="wb_Text2"
      style="
        position: absolute;
        left: 38px;
        top: 215px;
        width: 196px;
        height: 30px;
        z-index: 3;
      ">
      <p>Date: {date}</p>
    </div>
    <div
      id="wb_Text3"
      style="
        position: absolute;
        left: 38px;
        top: 260px;
        width: 175px;
        height: 30px;
        z-index: 4;
      ">
      <p>Time: {time}</p>
    </div>
    <div
      id="wb_Text4"
      style="
        position: absolute;
        left: 38px;
        top: 302px;
        width: 118px;
        height: 30px;
        z-index: 5;
      ">
      <p>gate: {gate}</p>
    </div>
    <div
      id="wb_Text5"
      style="
        position: absolute;
        left: 146px;
        top: 302px;
        width: 118px;
        height: 30px;
        z-index: 6;
      ">
      <p>Seat: {seat}</p>
    </div>
    <div
      id="wb_Image1"
      style="
        position: absolute;
        left: 213px;
        top: 71px;
        width: 489px;
        height: 244px;
        z-index: 7;
      ">
      <img src="872480.svg" id="Image1" alt="" width="489" height="245" />
    </div>
    <div
      id="wb_Text7"
      style="
        position: absolute;
        left: 459px;
        top: 21px;
        width: 159px;
        height: 37px;
        z-index: 9;

      ">
      <p>Bording pass</p>
    </div>
    <div
      id="wb_Text8"
      style="
        position: absolute;
        left: 721px;
        top: 17px;
        width: 142px;
        height: 22px;
        z-index: 10;
      ">
      <p>{airline_name}</p>
    </div>
    <div
      id="wb_Text9"
      style="
        position: absolute;
        left: 745px;
        top: 161px;
        width: 225px;
        height: 28px;
        z-index: 11;
      ">
      <p>Flight: {flight}</p>
    </div>
    <div
      id="wb_Text10"
      style="
        position: absolute;
        left: 745px;
        top: 204px;
        width: 182px;
        height: 28px;
        z-index: 12;
      ">
      <p>Date: {date}</p>
    </div>
    <div
      id="wb_Text11"
      style="
        position: absolute;
        left: 745px;
        top: 287px;
        width: 118px;
        height: 28px;
        z-index: 13;
      ">
      <p>gate: {gate}</p>
    </div>
    <div
      id="wb_Text12"
      style="
        position: absolute;
        left: 745px;
        top: 332px;
        width: 118px;
        height: 28px;
        z-index: 14;
      ">
      <p>Seat: {seat}</p>
    </div>
    <div
      id="wb_Text13"
      style="
        position: absolute;
        left: 745px;
        top: 245px;
        width: 118px;
        height: 28px;
        z-index: 15;
      ">
      <p>Time: {time}</p>
    </div>
    <hr
      id="HorizontalLine2"
      style="
        position: absolute;
        left: 692px;
        top: 67px;
        width: 299px;
        z-index: 16;
      " />
    <div
      id="wb_Line1"
      style="
        position: absolute;
        left: 707px;
        top: -4px;
        width: 3px;
        height: 386px;
        z-index: 17;
      ">
      <img src="images/img0001.png" id="Line1" alt="" width="0" height="386" />
    </div>
    <div
      id="wb_Text14"
      style="
        position: absolute;
        left: 745px;
        top: 83px;
        width: 225px;
        height: 45px;
        z-index: 18;
      ">
      <p>{fullname}</p>
    </div>
    <div
      id="wb_Image2"
      style="
        position: absolute;
        left: 9px;
        top: 17px;
        width: 78px;
        height: 45px;
        z-index: 19;
      ">
      <img
        src="{airline_logo}"
        id="Image2"
        alt="{airline_name}"
        width="78"
        height="45" />
    </div>
    <div
      id="wb_Text15"
      style="
        position: absolute;
        left: 98px;
        top: 17px;
        width: 166px;
        height: 22px;
        z-index: 20;
      ">
      <p>{airline_name}</p>
    </div>
    <div
      id="wb_Text6"
      style="
        position: absolute;
        left: 38px;
        top: 134px;
        width: 175px;
        height: 30px;
        z-index: 21;
      ">
      <p>To: {to}</p>
    </div>
    <div
      id="wb_Text16"
      style="
        position: absolute;
        left: 38px;
        top: 96px;
        width: 196px;
        height: 30px;
        z-index: 22;
      ">
      <p>From: {from_}</p>
    </div>
  </body>
</html>

"""
