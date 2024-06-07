namespace TutorinoAPICS.Models
{
    public class Corepetitions
    {
        public int zuid {get;set;}
        public int teacher {get;set;}
        public int pupil {get;set;}
        public int subject {get;set;}
        public int level {get;set;}
        public String status {get;set;}
        public DateTime start {get;set;}
        public DateTime end {get;set;}
        public int time {get;set;}
        public double price {get;set;}
        public String currency {get;set;}
        public char form {get;set;}
        public String meet_link {get;set;}
        public String table_link {get;set;}
        public String localization {get;set;}
        public bool accepted_o {get;set;}
        public bool accepted_k {get;set;}
        public bool paid_in_cash {get;set;}
        public int trainsaction_id {get;set;}
    }

    public class GetCorepet
    {
        public int zuid {get;set;}
    }

    public class NewCopepetition
    {
        public int teacher {get;set;}
        public int pupil {get;set;}
        public String subject {get;set;}
        public int level {get;set;}
        public String status {get;set;}
        public DateTime start {get;set;}
        public DateTime end {get;set;}
        public int time {get;set;}
        public double price {get;set;}
        public String currency {get;set;}
        public char form {get;set;}
        public String meet_link {get;set;}
        public String table_link {get;set;}
        public String localization {get;set;}
        public bool accepted_o {get;set;}
        public bool accepted_k {get;set;}
        public bool paid_in_cash {get;set;}
        public int trainsaction_id {get;set;}
    }

    public class EditCopepetition
    {
        public int zuid { get; set; }
        public int teacher { get; set; }
        public int pupil { get; set; }
        public String subject { get; set; }
        public int level { get; set; }
        public String status { get; set; }
        public DateTime start { get; set; }
        public DateTime end { get; set; }
        public int time { get; set; }
        public double price { get; set; }
        public String currency { get; set; }
        public char form { get; set; }
        public String meet_link { get; set; }
        public String table_link { get; set; }
        public String localization { get; set; }
        public bool accepted_o { get; set; }
        public bool accepted_k { get; set; }
        public bool paid_in_cash { get; set; }
        public int trainsaction_id { get; set; }
    }
}
