

export function formatDatetime(datetime){
    const datetimeOptions = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric"
  };

  var date = new Date(datetime)

  return date.toLocaleDateString('en-GB', datetimeOptions);

}