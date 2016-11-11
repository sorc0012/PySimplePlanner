BEGIN TRANSACTION;
CREATE TABLE workpackage (
	`wp_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`wp_taskid`	INTEGER NOT NULL,
	`wp_activity`	VARCHAR(20) NOT NULL,
	`wp_assignee`	TYPEVARCHAR(4),
	`wp_total_wl`	TYPEINTEGER,
	`wp_startdate`	TEXT NOT NULL,
	`wp_enddate`	TEXT NOT NULL,
	`wp_description`	VARCHAR(100),
	FOREIGN KEY(`wp_taskid`) REFERENCES `task`(`tsk_id`),
	FOREIGN KEY(`wp_activity`) REFERENCES `activitytype`(`type`),
	FOREIGN KEY(`wp_assignee`) REFERENCES `ressources`(`id`)
);
CREATE TABLE task (
	`tsk_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`tsk_name`	VARCHAR(40) NOT NULL UNIQUE,
	`tsk_projectid`	INTEGER NOT NULL,
	`tsk_startdate`	TEXT,
	`tsk_enddate`	TEXT,
	`tsk_description`	VARCHAR(100),
	`tsk_status`	TEXT NOT NULL DEFAULT "Not Validated",
	FOREIGN KEY(`tsk_projectid`) REFERENCES `project`(`prj_id`)
);
CREATE TABLE ressources (
                            id VARCHAR(4) PRIMARY KEY UNIQUE NOT NULL,
                            name VARCHAR(60)
                        );
CREATE TABLE project (
                        prj_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        prj_name VARCHAR(40) NOT NULL,
                        prj_startdate TEXT  NOT NULL,
                        prj_enddate TEXT  NOT NULL
                        );
CREATE TABLE imputations (
	`imp_wp_id`	TYPEINTEGER NOT NULL,
	`imp_wl`	TYPEINTEGER NOT NULL CHECK(0 < imp_wl < 8),
	`imp_date`	TYPETEXT NOT NULL,
	PRIMARY KEY(`imp_wp_id`,`imp_date`),
	FOREIGN KEY(`imp_wp_id`) REFERENCES `workpackage`(`wp_id`)
);
CREATE TABLE activitytype (
                        type VARCHAR(5) PRIMARY KEY UNIQUE NOT NULL,
                        description VARCHAR(60)
                        );
CREATE TRIGGER project_del_link DELETE ON project
	BEGIN
		DELETE FROM task WHERE tsk_projectid = old.prj_id;
	END;
CREATE TRIGGER task_del_link DELETE ON task
	BEGIN
		DELETE FROM workpackage WHERE wp_tskid = old.tsk_id;
	END;
CREATE TRIGGER workpackage_del_link DELETE ON workpackage
	BEGIN
		DELETE FROM imputations WHERE imp_wpid = old.wp_id;
	END;
COMMIT;
