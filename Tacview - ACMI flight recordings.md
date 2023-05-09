# Tacview - ACMI flight recordings

https://www.tacview.net/documentation/acmi/

## Technical Reference - ACMI flight recordings 2.2

### Introduction

![](https://wangtong15.oss-accelerate.aliyuncs.com/images/202305081401001.png)

With Tacview 1.5 a new universal public file format has been introduced. The goal was to overcome the complexity of the previous format while making it much more powerful at the same time.

Like its predecessor, the new file format is written in plain [UTF-8](https://en.wikipedia.org/wiki/UTF-8) text. That way, it is possible to easily export flight data from the simplest programming language. Its syntax is very easy to read by humans and, with the debug log introduced in Tacview 1.4.3, it is now very easy to diagnose any exporter issues. This new format is so simple that it could even be written by hand if the amount of data was not astronomic!

Despite its simplicity, the new format offers a very powerful way to set and change – in real-time – any property of any object on the battlefield. For instance, it is now possible to change the coalition, the color, even the type of an object, on the fly! In the same way, you can easily assign and change global properties, like the weather for example.

It is important to note that data which are not yet supported by Tacview are preserved and visible in the raw telemetry window. If you think that an important data should be natively supported and displayed by Tacview, feel free to [contact us](https://www.tacview.net/support/featurerequest).

> Tacview 1.5引入了一种新的通用公共文件格式。这是为了解决以前格式的复杂性，并在同一时间使其更加强大。
>
> 与其前身一样，新文件格式是以普通 [UTF-8](https://en.wikipedia.org/wiki/UTF-8) 文本编写的。这样，可以轻松地从最简单的编程语言中导出飞行数据。它的语法非常容易被人类阅读，而且在 Tacview 1.4.3 中引入的调试日志，现在非常容易诊断任何导出器问题。这种新格式非常简单，甚至可以手写，如果数据量不是天文数字的话！
>
> 尽管它很简单，但新格式提供了一种非常强大的方法来实时设置和更改战场上任何对象的任何属性。例如，现在可以在飞行中更改联盟、颜色，甚至对象的类型！同样地，您可以轻松地分配和更改全局属性，例如天气。
>
> 需要注意的是，Tacview尚不支持的数据在原始遥测窗口中得到保留和显示。如果您认为Tacview应该原生支持并显示重要数据，请[与我们联系](https://www.tacview.net/support/featurerequest)%E3%80%82

### ACMI 2.2 File Format 101

Without further ado, let's start with the simplest file possible:
不再多言，让我们从可能的最简单的文件开始：

```
FileType=text/acmi/tacview
FileVersion=2.2
```

These are the only two mandatory lines you must put first in any ACMI file. This header tells Tacview which format to expect. Any following data is optional.

> 这是在任何ACMI文件中必须放在最前面的两行。此标头告诉Tacview要期望的格式。任何随后的数据都是可选的。

Let's be rational: Even if Tacview will gracefully load this empty file, we need a bit more data to make it useful! Here is a file which makes more sense:

> 让我们理性一点：即使Tacview会优雅地加载这个空文件，我们仍需要更多的数据使其有用！以下是一个更有意义的文件：

```
FileType=text/acmi/tacview
FileVersion=2.2
0,ReferenceTime=2011-06-02T05:00:00Z
#47.13
3000102,T=41.6251307|41.5910417|2000.14,Name=C172
```

To better understand this structure, we need to know that – apart from its header – each line of the file can be either:

-   The sharp sign # introducing a new time frame in seconds relative to ReferenceTime
-   An object id (in this example 0 and 3000102) followed by as many properties as you want separated by commas ,. Each property will be assigned a new value using the equal sign \=.
-   The third possibility – not shown here – is a line which starts with the minus sign \- followed by the id of an object we want to remove from the battlefield (could be destroyed or simply out of recording range).

Let's see in detail each line syntax:

> 为了更好地理解这种结构，我们需要知道除了文件头之外，文件的每一行可以是以下任一一种情况：
>
> - `#`号开头，表示相对于参考时间的新时间段（以秒为单位）
> - 对象ID（在这个例子中为0和3000102），后面跟着您想要分隔的任意数量的属性，用逗号，分隔。每个属性都将使用等号=赋予一个新值。
> - 第三种可能性-此处未显示-是以减号-开头的行，后面跟着我们想要从战场上移除的对象的ID（可能被摧毁或仅仅是超出记录范围）。
>
> 让我们详细看一下每行的语法：

```
0,ReferenceTime=2011-06-02T05:00:00Z
```

This line assigns the value 2011-06-02T05:00:00Z to the property ReferenceTime of the global object always designated by its id zero 0. In other words: This line defines the base/reference time used for the whole flight recording. To understand better what this means, let's have a look at the following line:

> 这行代码将值2011-06-02T05:00:00Z赋给了全局对象的参考时间属性，该全局对象始终由其ID零0表示。换句话说，这行代码定义了整个飞行记录使用的基准/参考时间。为了更好地理解这意味着什么，让我们看看下面这行代码：


```
#47.13
```

This line defines a time-frame in seconds relative to ReferenceTime. In that case, this means that the following events or properties happened at ReferenceTime + 47.13 seconds ⇒ 2011-06-02T05:00:00Z + 47.13 ⇒ 2011-06-02T05:00:47.13Z

> 这行代码定义了一个相对于ReferenceTime的时间段（以秒为单位）。在这种情况下，这意味着以下事件或属性发生在ReferenceTime + 47.13秒处⇒2011-06-02T05:00:00Z + 47.13⇒2011-06-02T05:00:47.13Z。

Now let's see the following line:

```
3000102,T=41.6251307|41.5910417|2000.14,Name=C172
```

This line defines two properties for the object 3000102. To save space, Object ids are expressed in [hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal) without any prefix or leading zeros.

The first property T (which stands for Transform) is a special property used to define the object coordinates in space. We will see later which syntaxes are supported for T. For now, let's just focus on this case which is: T = Longitude | Latitude | Altitude.

Notice that Latitude and Longitude are expressed in degrees. Positive values are toward the north and east directions. Since the whole file is always in the metric system, the altitude is expressed in meters [MSL](https://en.wikipedia.org/wiki/Metres_above_sea_level) (above sea level, also known as ASL in some countries).

The following property Name obviously defines the object name C172 which is a short way of designating a [Cessna 172](https://en.wikipedia.org/wiki/Cessna_172) aircraft.

Now that you know all the basics to create a flight recording, let's move our new aircraft a bit further to the east. To do so, we can simply add another frame to our file:

> 这行代码为3000102对象定义了两个属性。为了节省空间，对象ID以十六进制表示，没有任何前缀或前导零。
>
> 第一个属性T（代表变换）是一个特殊属性，用于定义物体在空间中的坐标。稍后我们将看到支持T的哪些语法。现在，我们只需要关注这种情况，即：T = 经度 | 纬度 | 高度。
>
> 注意，纬度和经度以度数表示。正值朝向北和东方向。由于整个文件始终使用公制系统，高度以海拔高度（上面链接有解释）（MSL）以米为单位表示。
>
> 以下属性Name显然定义了物体名称C172，这是指代[Cessna 172](https://en.wikipedia.org/wiki/Cessna_172)
>
> 现在你已经了解了创建飞行记录的所有基础知识，让我们将我们的新飞机向东移动一些。为此，我们可以简单地在文件中添加另一个帧：



```
#49
3000102,T=41.626||
```

As you can see, we have defined a new longitude value 41.626 for our aircraft at the time frame 2011-06-02T05:00:49Z

You may have noticed that we don't need to specify – again – the aircraft name, simply because it has not changed since the last time! Another difference with the previous record is that we have omitted the latitude and altitude parameters because they did not change either. This helps to save a lot of space when generating data for long flights. While aircraft are usually quite mobile, this optimization is especially relevant for ground objects which can stay still or move just a little bit time to time...

> 正如您所看到的，我们在2011年06月02日05:00:49Z期间为我们的飞机定义了一个新的经度值41.626。
>
> 您可能已经注意到，我们无需再次指定飞机名称，这是因为它自上次以来没有更改！与以前的记录的另一个区别在于，我们省略了纬度和高度参数，因为它们也没有更改。当生成长时间飞行的数据时，这有助于节省大量空间。虽然飞机通常相当活动，但这种优化尤其适用于地面物体，它们可以保持静止或偶尔移动一点点时间......

### Detailed File Specifications

Now that you are starting to understand better how ACMI files are structured, let's review together the requirements and some tips related to the file format in general:

> 现在您已经开始更好地理解ACMI文件的结构，让我们一起回顾一下与文件格式相关的要求和一些提示

#### Requirements

-   Text data must be written in UTF-8. That way, all languages are supported for text properties. 文本数据必须以UTF-8格式编写。这样，所有语言的文本属性都得到支持。
-   All data are expressed in the metric system, using meters, meters per second for speed, degrees for angles, [UTC time](https://en.wikipedia.org/wiki/Coordinated_Universal_Time) and so on. 所有数据都使用公制系统表示，使用米、每秒米为速度，角度为度，[协调世界时]
-   Object ids are expressed using 64-bit hexadecimal numbers (without prefix or leading zeros to save space) 对象 ID 采用64位十六进制数字表示（无需前缀或前导零以节省空间）。
-   The object 0 is used to define global properties (like ReferenceTime or Briefing) 对象0用于定义全局属性（如ReferenceTime或Briefing）。
-   When you want to assign a text property which contains a comma , you must put the escape character \\ before it so it is not interpreted by Tacview as the end of your string. 当您想要分配包含逗号“，”的文本属性时，必须在逗号前放置转义字符“\”，以便Tacview不会将其解释为字符串的结束。

```
Briefing=Here is a text value\, which contains an escaped comma in it!
```

#### Tips

-   To save space, it is strongly suggested to end lines with the LF \\n character only.
-   It is cleaner to prefix text data with the UTF-8 [BOM](https://en.wikipedia.org/wiki/Byte_order_mark) header.
-   The whole of the text data can be wrapped in a zip or 7z container to save bandwidth or disk space.
-   Data can be presented out-of-order. Tacview will do its best to reorder it in memory.

### Object Coordinates

Now let's have a closer look at the different notations for object coordinates. To optimize the file size, Tacview offers four different notations.

> 现在让我们更仔细地看一下物体坐标的不同标记法。为了优化文件大小，Tacview提供四种不同的标记法。 

Here are two examples: When exporting a bullet coordinate, we do not need any data about its rotation angles. The opposite example would be an aircraft in a flight simulator running in a flat world like Falcon 4.0: In that case, to get accurate replay, we should export the native position of the aircraft in the flat world, its rotation, and its coordinates in a spherical world. That way the aircraft will not only be properly displayed in Tacview's spherical world, but telemetry calculation will be done in the object's native coordinate system so the numbers visible on screen will match the ones you can see in the original flight simulator.

> 这里有两个例子：当导出子弹坐标时，我们不需要任何与其旋转角度相关的数据。相反的例子是在像Falcon 4.0这样的平面世界中运行的飞行模拟器中的飞机：在这种情况下，为了获得准确的回放，我们应该导出飞机在平面世界中的原始位置、旋转和在球形世界中的坐标。这样，飞机不仅会在Tacview的球形世界中正确显示，而且遥测计算将在物体的本地坐标系中完成，因此屏幕上可见的数字将与在原始飞行模拟器中看到的数字匹配。



T = Longitude | Latitude | Altitude

Simple objects in a spherical world (typically minor objects like bullets). Can also be relevant for low-end data source like GPX files without rotation information.

> 在球形世界中的简单物体（通常是像子弹一样的小物体）。也适用于像GPX文件这样没有旋转信息的低端数据源。



T = Longitude | Latitude | Altitude | U | V

Simple objects from a flat world. U & V represent the native x and y. Do not forget to express them in meters even if the original coordinates are in feet for example. Altitude is not repeated because it is the same for both native and spherical worlds.

> 简单的物体来自一个平坦的世界。U和V代表本地的x和y。即使原始坐标是英尺，也不要忘记以米为单位表示它们。高度不被重复，因为它在本地和球形世界中是相同的。



T = Longitude | Latitude | Altitude | Roll | Pitch | Yaw

Complex objects in a spherical world. Roll is positive when rolling the aircraft to the right. Pitch is positive when taking-off. Yaw is clockwise relative to the true north.

> 球形世界中的复杂物体。将飞机向右滚动时，滚动为正值。起飞时俯仰为正值。偏航相对于真北方向为顺时针。



T = Longitude | Latitude | Altitude | Roll | Pitch | Yaw | U | V | Heading

Complex object from a flat world. Same as before. Heading is the yaw relative to the true north of the flat world. It is required because the native world north usually does not match spherical world north because of projection errors.

Remember that you can omit the components which did not change since the last time. This will save a lot of space.

If some of the data is missing (for example object rotation), Tacview will do its best to emulate it in order to give a nice replay. Independently from optimization, you should keep the same data notation for each object during the object life. If at one point you use a different notation, Tacview will do its best to promote the object to a more complex one. However – because of the initial lack of data – the final result may not be the expected one.

> 复杂物体来自一个平面世界，与之前一样。航向是相对于平面世界真正北方的偏航角。这是必需的，因为本地世界北方通常不符合球形世界的北方，因为投影误差。
>
> 请记住，您可以省略自上次以来未发生变化的部分。这将节省大量空间。
>
> 如果一些数据缺失（例如物体旋转），Tacview会尽力模拟它，以便提供一个漂亮的回放。无论如何优化，您都应该在对象的整个生命周期内保持相同的数据表示法。如果在某个时刻您使用了不同的符号表示法，Tacview会尽力将对象升级为更复杂的对象。然而，由于最初缺乏数据，最终结果可能不是预期的。

### Global Properties

We already saw that one of the most important global properties is the ReferenceTime. Obviously, there are plenty of other meta-data you can inject in a flight recording to make your replay more detailed.

> 我们已经看到，最重要的全局属性之一是ReferenceTime。显然，您可以注入许多其他元数据到飞行记录中，以使您的回放更加详细。

#### Text Properties

| Property Name | Meaning                                                      |
| :------------ | :----------------------------------------------------------- |
| DataSource    | Source simulator, control station or file format.<br /> `DataSource=DCS 2.0.0.48763` <br />`DataSource=GPX File`<br />源仿真器、控制站或文件格式 |
| DataRecorder  | Software or hardware used to record the data. `DataRecorder=Tacview 1.5` <br />`DataRecorder=Falcon 4.0` |
| ReferenceTime | Base time (UTC) for the current mission. This time is combined with each frame offset (in seconds) to get the final absolute UTC time for each data sample.<br />`ReferenceTime=2011-06-02T05:00:00Z` |
| RecordingTime | Recording (file) creation (UTC) time. <br />`RecordingTime=2016-02-18T16:44:12Z` |
| Author        | Author or operator who has created this recording. <br />`Author=Lt. Cmdr. Rick 'Jester' Heatherly` |
| Title         | Mission/flight title or designation. <br />`Title=Counter Attack` |
| Category      | Category of the flight/mission. <br />`Category=Close air support` |
| Briefing      | Free text containing the briefing of the flight/mission. `Briefing=Destroy all SCUD launchers` |
| Debriefing    | Free text containing the debriefing. <br />`Debriefing=Managed to stay ahead of the airplane.` |
| Comments      | Free comments about the flight. Do not forget to escape any end-of-line character you want to inject into the comments. <br />`Comments=Part of the recording is missing because of technical difficulties.` |

> Briefing是包含任务简报的文本，其中包含任务目标、任务类型、天气、任务简述以及其他必要的信息。它主要用于帮助玩家了解和准备任务。 
>
> Debriefing是跟随任务完成后的结果，包含任务完成情况、任务目标是否达成等信息。它主要用于评估任务完成的效果和表现，并基于此提供反馈和建议。在DCS World中，Briefing和Debriefing等信息都是由任务创建者或任务发布者编写和设定的。
> 
> ReferenceTime是当前任务的基准时间（UTC），每个帧偏移量（以秒为单位）与它相结合，以获取每个数据样本的最终绝对UTC时间。
> 
> 而RecordingTime是录制（文件）创建（UTC）时间。它们的区别在于一个是基准时间，一个是文件创建时间。



#### Numeric Properties

| Property Name                        | Unit | Meaning                                                      |
| :----------------------------------- | :--- | :----------------------------------------------------------- |
| ReferenceLongitude ReferenceLatitude | deg  | These properties are used to reduce the file size by centering coordinates around a median point. They will be added to each object Longitude and Latitude to get the final coordinates. <br />ReferenceLongitude=-129<br /> ReferenceLatitude=43<br />这些属性被用于通过将坐标中心化到一个中位数点来减小文件大小。它们将被添加到每个对象的经度和纬度上，以获得最终的坐标 |

#### Events

Events can be used to inject any kind of text, bookmark and debug information into the flight recording. They are a bit special: They are declared like properties, but unlike properties, you can declare several events in the same frame without overriding the previous one.

> 事件可以用于注入任何类型的文本、书签和调试信息到飞行记录中。它们有点特殊：它们声明类似于属性，但与属性不同的是，您可以在同一帧中声明多个事件而不会覆盖以前的事件。

Here is an example on how to inject events:

```
#8.62
0,Event=Message|3000100|Here is a generic event linked to the object 3000100
0,Event=Bookmark|Here is a bookmark to highlight a specific part of the mission!
#8.72
0,Event=Debug|Here is some debug text, visible only with the /Debug:on command line option
```

You may notice the structure of an event declaration:

```
Event = EventType | FirstObjectId | SecondObjectId | ... | EventText
```

For each event we must declare first the type of the event (e.g. Bookmark), optionally followed by ids of concerned objects. For example, when the user double click on the event, Tacview will use theses ids to automatically center the camera around associated objects. The last part is a mandatory text message. Even if it is possible to provide an empty text, it is suggested to provide a useful message to get the most out of your debriefings.

> 对于每个事件，我们必须首先声明事件的类型（例如，书签），可选地跟随相关对象的ID。例如，当用户双击事件时，Tacview将使用这些ID自动将相机对准相关对象。最后一部分是必需的文本消息。即使可以提供空文本，建议提供有用的消息以充分利用您的复盘。

Here are the different kind of events currently supported by Tacview:

| Event Name | Meaning                                                      |
| :--------- | :----------------------------------------------------------- |
| Message    | Generic event. 0,Event=Message\|705\|Maverick has violated ATC directives |
| Bookmark   | Bookmarks are highlighted in the time line and in the event log. They are easy to spot and handy to highlight parts of the flight, like a bombing run, or when the trainee was in her final approach for landing. 0,Event=Bookmark\|Starting precautionary landing practice |
| Debug      | Debug events are highlighted and easy to spot in the timeline and event log. Because they must be used for development purposes, they are displayed only when launching Tacview with the command line argument /Debug:on 0,Event=Debug\|327 active planes |
| LeftArea   | This event is useful to specify when an aircraft (or any object) is cleanly removed from the battlefield (not destroyed). This prevents Tacview from generating a Destroyed event by error. 0,Event=LeftArea\|507\| |
| Destroyed  | When an object has been officially destroyed. 0,Event=Destroyed\|6A56\| |
| TakenOff   | Because Tacview may not always properly auto-detect take-off events, it can be useful to manually inject this event in the flight recording. 0,Event=TakenOff\|2723\|Col. Sinclair has taken off from Camarillo Airport |
| Landed     | Because Tacview may not always properly auto-detect landing events, it can be useful to manually inject this event in the flight recording. 0,Event=Landed\|705\|Maverick has landed on the USS Ranger |
| Timeout    | Mainly used for real-life training debriefing to specify when a weapon (typically a missile) reaches or misses its target. Tacview will report in the shot log as well as in the 3D view the result of the shot. Most parameters are optional. SourceId designates the object which has fired the weapon, while TargetId designates the target. Even if the displayed result may be in nautical miles, bullseye coordinates must be specified in meters. The target must be explicitly (manually) destroyed or disabled using the appropriate properties independently from this event. 0,Event=Timeout\|SourceId:507\|AmmoType:FOX2\|AmmoCount:1\|Bullseye:50/15000/2500\|TargetId:201\|IntendedTarget:Leader\|Outcome:Kill |

![image-20230508152001186](https://wangtong15.oss-accelerate.aliyuncs.com/images/202305081520229.png)

| 事件名称 | 意义                                                         |
| :------- | :----------------------------------------------------------- |
| Message  | 通用事件。0，Event=Message|
| Bookmark | 书签在时间轴和事件日志中突出显示。它们很容易发现，可以方便地突出显示飞行的某些部分，例如轰炸行动，或练习引导接近着陆。 |
| Debug    | 调试事件在时间轴和事件日志中突出显示并易于发现。因为它们必须用于开发目的，所以仅在使用命令行参数/Debug:on启动Tacview时才显示。 |
| LeftArea | 此事件用于指定当飞机（或任何对象）已清除战场时（未被摧毁），这可防止Tacview因错误而生成销毁事件。0，Event=LeftArea|
| Destroyed | 当对象被正式销毁时。 |
| TakenOff | 因为Tacview可能不总是正确自动检测起飞事件，所以手动插入此事件到飞行记录中会很有用。 |
| Landed   | 因为Tacview可能不总是正确自动检测着陆事件，所以手动插入此事件到飞行录像中会很有用。 |
| Timeout  | 主要用于现实生活的培训反馈，以指定武器（通常是导弹）到达或未击中目标的时间。Tacview将在射击日志中报告以及在3D视图中显示射击结果。大多数参数是可选的。SourceId指定发射武器的对象，而TargetId则指定目标。即使显示的结果可能是海里，中心点坐标必须以米为单位指定。必须使用适当的属性显式（手动）摧毁或禁用目标，而不是使用此事件。 |



### Object Properties

Since Tacview 1.5, it is possible to set and change any object property in real-time. Even if new properties may not always be visible in the 3D view, you can always have a look at the raw telemetry window to see what is the current value of each property for currently selected objects.

> 自 Tacview 1.5 版本起，您可以实时设置和更改任何对象属性。即使新属性并不总是在 3D 视图中可见，您仍然可以查看原始遥测窗口，了解当前选择对象的每个属性的当前值。 

Tacview 1.7 has introduced a new object [database](https://www.tacview.net/documentation/database/en/) which enables you to predefine any of the object properties expect for **Type** and **Name**. For example, you can predefine the default **shape** of a **F-16C** in that database. If the **Shape** property value is not defined in the telemetry file, Tacview will use the value stored in the database and display your custom 3D model for the F-16C in the 3D view.

> Tacview 1.7 版本引入了新的数据库对象，可以预定义任何物体属性（除 Type 和 Name 外）。例如，您可以在该数据库中预定义 F-16C 的默认形状。如果遥测文件中未定义“形状”属性值，则 Tacview 将使用存储在数据库中的值，并在 3D 视图中显示您自定义的 F-16C 的 3D 模型。

Learn how to update and extend Tacview database by reading the [dedicated documentation](https://www.tacview.net/documentation/database/en/).

#### Text Properties

| Property Name                     | Meaning                                                      |
| :-------------------------------- | :----------------------------------------------------------- |
| Name                              | The object name should use the most common notation for each object. It is strongly recommended to use [ICAO](https://www.icao.int/publications/DOC8643/Pages/Search.aspx) or [NATO](https://en.wikipedia.org/wiki/NATO_reporting_name) names like: C172 or F/A-18C. This will help Tacview to associate each object with the corresponding entry in its database. Type and Name are the only properties which *CANNOT* be predefined in Tacview [database](https://www.tacview.net/documentation/database/en/). <br />`Name=F-16C-52`<br />对象名称应使用每个对象的最常见符号表示。强烈建议使用ICAO或NATO名称如：C172或F/A-18C。这将帮助Tacview将每个对象与其数据库中相应的条目关联起来。"Type"和 "Name" 是Tacview数据库中 *不能* 预定义的唯一属性。<br />ICAO指的是国际民航组织（International Civil Aviation Organization），是联合国下属的一个国际组织，负责管理全球民航事务和相关标准。NATO指的是北约（North Atlantic Treaty Organization），是由北美和欧洲国家组成的军事联盟。在航空和飞行器领域，这两个缩写通常用来指代特定型号的飞机。例如，F/A-18C就是一种北约飞机型号。 |
| Type                              | Object types are built using tags. This makes object management much more powerful and transparent than with the previous exclusive types. (see below for the list of supported types). Type and Name are the only properties which *CANNOT* be predefined in Tacview [database](https://www.tacview.net/documentation/database/en/). <br />`Type=Air+FixedWing`<br />  对象类型是使用标签构建的。这使得对象管理比以前的独占类型更加强大和透明（请参见下面支持的类型列表）。类型和名称是 *不能* 在Tacview数据库中预定义的唯一属性。 |
| AdditionalType                    | Any tags defined here will be added to the current object Type. This is useful to force an object type which has not been defined explicitly in the telemetry data. For example, you can use this property to automatically set the FixedWing tag for a Cessna 172 telemetry data which come from a Garmin csv file (which usually does not contain any type declaration). For obvious reasons, this property must be used only in Tacview database, *NOT* in telemetry files. <br />`<AdditionalType>Air+FixedWing</AdditionalType>`<br />在此定义的任何标签都将添加到当前对象类型中。这对于强制一个未在遥测数据中明确定义的对象类型非常有用。例如，您可以使用此属性自动为来自Garmin csv文件的Cessna 172遥测数据设置FixedWing标签（该文件通常不包含任何类型声明）。由于明显的原因，此属性必须仅在Tacview数据库中使用，*而不是*在遥测文件中使用。 |
| Parent                            | Parent hexadecimal object id. Useful to associate for example a missile (child object) and its launcher aircraft (parent object). `Parent=2D50A7`<br />父十六进制对象ID。用于将导弹（子对象）与其发射飞机（父对象）关联起来非常有用 |
| Next                              | Hexadecimal id of the following object. Typically used to link waypoints together. <br />`Next=40F1`<br />以下对象的十六进制 ID 。通常用于将航点连接在一起。 |
| ShortName                         | This abbreviated name will be displayed in the 3D view and in any other cases with small space to display the object name. Typically defined in Tacview database. Should not be defined in telemetry data. `ShortName=A-10C`<br />这个缩写名称将会在3D视图和其他空间较小的情况下显示对象名称。通常在Tacview数据库中定义。不应该在遥测数据中定义。 |
| LongName                          | More detailed object name, used in small windows where there is more space than in a cluttered 3D view, but not enough space to display the full detailed name. For readability, it is suggested to start by the short name first (usually an abbreviation like the NATO code), followed by the object nickname / NATO name. Typically defined in Tacview database. Should not be defined in telemetry data. <br />`LongName=A-10C Thunderbolt II`<br />更详细的对象名称，适用于小窗口，在那里比杂乱的3D视图有更多的空间，但不足以显示完整的详细名称。为了可读性，建议首先从短名称开始（通常是NATO代码的缩写），然后是对象昵称/ NATO名称。通常在Tacview数据库中定义。不应在遥测数据中定义 |
| FullName                          | The full object name which is typically displayed in windows and other logs wherever there is enough space to display a lot of data without clutter issues. Typically defined in Tacview database. Should not be defined in telemetry data.<br /> `FullName=Fairchild Republic A-10C Thunderbolt II`<br />完整的对象名称通常在Windows和其他日志中显示，无需担心杂乱问题显示大量数据的空间。通常在Tacview数据库中定义。不应在遥测数据中定义 |
| CallSign                          | The call sign will be displayed in priority over the object name and sometimes pilot name, especially in the 3D view and selection boxes. This is handy for mission debriefings where call signs are more informative than aircraft names. <br />`CallSign=Jester`<br />呼号将具有优先于对象名称和飞行员名称的显示，特别是在3D视图和选择框中。这对于任务总结很方便，因为呼号比飞机名称更具有信息量<br /> 呼号（callsign）是指为个人或组织指定的独特名称或符号，通常用于识别无线电、电话或其他电子通信交互中的发送或接收方。在航空交通控制等领域中，呼号通常用于识别不同的航班、飞机或航空公司。例如，"United 123"是一个常见的航班呼号，"Delta 456"是另一个航班呼号。呼号在飞行中非常重要，因为它可以帮助管制员快速识别飞机的身份和位置，有助于确保空中安全。在实时战略游戏中，呼号通常用于标识不同的单位或玩家。 |
| Registration                      | 给 #dcs-master 发消息Aircraft registration (aka tail number) <br />`Registration=N594EX`<br />飞机注册号（也称为机尾号码） |
| Squawk                            | Current transponder code. Any code is possible, there is no limitation like with the old 4 digit transponders. <br />`Squawk=1200`<br />目前的转发器代码。任何代码都可以，与旧的4位转发器不同，没有限制 |
| ICAO24                            | Mode S equipped aircraft uniquely assigned ICAO 24-bit address. <br />`ICAO24=A72EC8`<br />配备了S模式的飞机具有唯一的ICAO 24位地址。 |
| Pilot                             | Aircraft pilot in command name. <br />`Pilot=Iceman`<br />机长姓名。 |
| Group                             | Group the object belongs to. Used to group objects together. For example, a formation of F-16 flying a CAP together. <br />`Group=Springfield`<br />对象所属的组。用于将对象分组。例如，一群F-16飞机共同执行战斗机护航任务。 |
| Country                           | [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country code. Country=us |
| Coalition                         | Coalition <br />`Coalition=Allies`                           |
| Color                             | Can be one of the following: Red, Orange, Yellow (Tacview 1.8.8), Green, Cyan (Tacview 1.8.8), Blue, Violet. Colors are predefined to ensure a clear display of the whole battlefield in all conditions. `Color=Blue`<br />可以是以下颜色之一：红色，橙色，黄色（Tacview 1.8.8），绿色，青色（Tacview 1.8.8），蓝色，紫色。颜色被预定义以确保在所有条件下都可以清晰地显示整个战场。 |
| Shape                             | Filename of the 3D model which will be used to represent the object in the 3D view. 3D models must be in [Wavefront .obj file format](https://en.wikipedia.org/wiki/Wavefront_.obj_file) and stored in either %ProgramData%\Tacview\Data\Meshes\ or %APPDATA%\Tacview\Data\Meshes\. Learn more about 3D models by reading the [dedicated documentation](https://www.tacview.net/documentation/3dobjects/en/) <br />`Shape=Rotorcraft.Bell 206.obj`<br />用于在 3D 视图中呈现物体的 3D 模型的文件名。3D 模型必须是 Wavefront .obj 文件格式，并存储在 %ProgramData%\Tacview\Data\Meshes\ 或 %APPDATA%\Tacview\Data\Meshes\ 中。 通过阅读专门的文档，了解更多关于 3D 模型的信息。 |
| Debug                             | Debug text visible in the 3D view when Tacview is launched with the /Debug:on command line argument. <br />`Debug=ObjectHandle:0x237CB9`<br />当使用/Debug:on命令行参数启动Tacview时，在3D视图中可见调试文本。 |
| Label                             | Free real-time text displayable in the 3D view and telemetry windows (to provide miscellaneous info to the end-user) <br />`Label=Lead aircraft`<br />免费实时文本显示在3D视图和遥测窗口中（向最终用户提供杂项信息） |
| FocusedTarget                     | Target currently focused by the object (typically used to designate laser beam target object, can also be used to show what the pilot is currently focused on) <br />`FocusedTarget=3001200`<br />当前由对象聚焦的目标（通常用于指定激光束目标对象，也可以用于显示飞行员当前聚焦的内容） |
| `LockedTarget `to `LockedTarget9` | Primary target hexadecimal id (could be locked using any device, like radar, IR, NVG, ...) <br />`LockedTarget2=3001200`<br />首要目标的十六进制ID（可以使用任何设备（如雷达，红外线，夜视仪等）进行锁定） |




#### Numeric Properties

| Property Name                                                | Unit    | Meaning                                                      |
| :----------------------------------------------------------- | :------ | :----------------------------------------------------------- |
| Importance                                                   | ratio   | The higher the ratio, the more important is the object is (e.g. locally simulated aircraft could be 1.0 importance factor)<br />`Importance=1`<br />重要性因素越高，对象就越重要（例如，本地模拟飞机的重要性因素可能为1.0） |
| Slot                                                         | index   | Plane position in its Group (the lowest is the leader) <br />`Slot=0`<br />飞机在其编队中的位置（最低的是领航员） |
| Disabled                                                     | boolean | Specifies that an object is disabled (typically out-of-combat) without being destroyed yet. This is particularly useful for combat training and shotlogs. `Disabled=1`<br />指定对象在尚未被摧毁的情况下被禁用（通常是在战斗之外）。这在战斗训练和射击记录中特别有用。 |
| Visible                                                      | ratio   | This property is useful to hide specific objects from the 3D view. Can be used for a fog-of-war effect, or to prevent virtual objects from being displayed. When set to 1, the object is fully visible. When set to 0, the object is invisible and may be omitted from objects lists. <br />`Visible=0.333`<br />这个属性用于从三维视图中隐藏特定对象。可以用于制造战争迷雾效果，或防止虚拟对象被显示。当设置为1时，对象是完全可见的。当设置为0时，对象是看不见的，可能被从对象列表中省略。 |
| Health                                                       | ratio   | Use this attribute to record the current health status of an object. The ratio is equal to 1.0 when the object is brand new, and 0.0 whenever the object is out of combat/dead/destroyed. This attribute as currently no effect on the events, you still need to remove the object manually whenever it is destroyed. <br />`Health=0.84`<br />使用这个属性记录对象的当前健康状态。当对象全新时，比率等于1.0，当对象处于战斗/死亡/摧毁状态时，比率为0.0。该属性目前对事件没有影响，仍需手动删除对象 |
| Length                                                       | m       | Object length. Especially useful when displaying buildings. <br />`Length=20.5`<br />对象长度。在显示建筑物时尤其有用 |
| Width                                                        | m       | Object width. Especially useful when displaying buildings. <br />`Width=10.27` |
| Height                                                       | m       | Object height. Especially useful when displaying buildings.<br />`Height=4` |
| Radius                                                       | m       | Object bounding sphere radius. Object bounding sphere radius. Can be used to define custom explosion, smoke/grenade radius. Can be animated. <br />`Radius=82`<br />物体包围球半径。物体包围球半径。可用于定义自定义的爆炸，烟雾/手榴弹半径。可进行动画处理 |
| IAS                                                          | m/s     | Indicated airspeed <br />`IAS=69.4444`<br />指示空速         |
| CAS                                                          | m/s     | Calibrated airspeed <br />`CAS=250`<br />校准空速            |
| TAS                                                          | m/s     | True airspeed <br />`TAS=75`<br />真空速                     |
| Mach                                                         | ratio   | Mach number <br />`Mach=0.75`<br />马赫数                    |
| AOA                                                          | deg     | Angle of attack <br />`AOA=15.7`<br />AOA (Angle of Attack) 是指飞机相对于气流的进出角度。它是一项非常重要的飞行指标，在飞行中用于监测飞机的飞行状态。过高或过低的 AOA 都可能会导致飞机进入危险状态，因此飞行员需要时刻关注并控制 AOA。在模拟飞行游戏 DCS World 中，也需要考虑和控制 AOA 以获得更稳定、安全的飞行体验。 |
| AOS                                                          | deg     | Sideslip angle, also called angle of sideslip `AOS=5.2`<br />侧滑角，也叫侧滑角度 |
| AGL                                                          | m       | Object altitude above ground level `AGL=1501.2`<br />物体离地高度 |
| HDG                                                          | deg     | Aircraft heading. When there is no roll and pitch data available, this property can be used to specify the yaw while keeping full rotation emulation in the 3D view. <br />HDG=185.3<br />飞机航向。当没有可用的滚转和俯仰数据时，可以使用该属性来指定偏航，同时保持物体在三维视图中的完全旋转仿真。 |
| HDM                                                          | deg     | Aircraft magnetic heading. Heading relative to local magnetic north. <br />`HDM=187.3`<br />飞机磁头航向。相对于当地磁北极的航向 |
| Throttle <br />Throttle2                                     | ratio   | Engine 1 & 2 throttle handle position (could be >1 for Afterburner and <0 for reverse) <br />`Throttle=0.75`<br />发动机1和2的油门手柄位置（在加力燃烧室中可能大于1，在倒退中可能小于0） |
| EngineRPM <br />EngineRPM2                                   | RPM     | Engine 1 & 2 speed in RPM (revolutions per minute) <br />`EngineRPM=1500`<br />发动机1和2转速为RPM（每分钟转数） |
| Afterburner                                                  | ratio   | Main/engine #1 afterburner status<br /> `Afterburner=1`<br /> 主/1号引擎加力器状态 |
| AirBrakes                                                    | ratio   | Air brakes status <br />`AirBrakes=0`<br />气闸状态          |
| Flaps                                                        | ratio   | Flaps position <br />`Flaps=0.4`<br />襟翼位置               |
| LandingGear                                                  | ratio   | Landing gear status <br />`LandingGear=1`<br />起落架状态    |
| LandingGearHandle                                            | ratio   | Landing gear handle position `LandingGearHandle=0`<br />起落架手柄位置 |
| Tailhook                                                     | ratio   | Arresting hook status <br />`Tailhook=1`<br />阻拦钩状态     |
| Parachute                                                    | ratio   | Parachute status (not to be mistaken for DragChute) <br />`Parachute=0`<br />降落伞状态（与拖曳伞不要混淆） |
| DragChute                                                    | ratio   | Drogue/Drag Parachute status `DragChute=1`                   |
| `FuelWeight`<br />to <br />`FuelWeight9`                     | kg      | Fuel quantity currently available in each tanks (up to 10 tanks supported). <br />`FuelWeight4=8750`<br />每个油箱当前可用燃油质量（支持最多10个油箱） |
| `FuelVolume`<br />to <br />`FuelVolume9`                     | l       | Fuel quantity currently available in each tanks (up to 10 tanks supported). `FuelVolume=75`<br />每个油箱当前可用燃油容量（支持最多10个油箱） |
| `FuelFlowWeight`<br />to `FuelFlowWeight8`                   | kg/hour | Fuel flow for each engine (up to 8 engines supported). `FuelFlowWeight2=38.08`<br />每个发动机燃油流量（支持最多8个发动机） |
| `FuelFlowVolume` <br />to <br />`FuelFlowVolume8`            | l/hour  | Fuel flow for each engine (up to 8 engines supported). FuelFlowVolume2=53.2 |
| RadarMode                                                    | number  | Radar mode (0 = off) <br />`RadarMode=1`<br />雷达模式       |
| RadarAzimuth                                                 | deg     | Radar azimuth (heading) relative to aircraft orientation <br />`RadarAzimuth=-20`<br /> 雷达方位角（航向）相对于飞机方向 |
| RadarElevation                                               | deg     | Radar elevation relative to aircraft orientation <br />`RadarElevation=15`<br />雷达俯仰角（相对于飞机方向的俯仰） |
| RadarRoll                                                    | deg     | Radar roll angle relative to aircraft orientation <br />`RadarRoll=-45`<br />雷达滚转角（相对于飞机方向的滚转） |
| RadarRange                                                   | m       | Radar scan range <br />`RadarRange=296320`<br />雷达扫描范围 |
| RadarHorizontalBeamwidth                                     | deg     | Radar beamwidth in azimuth <br />`RadarHorizontalBeamwidth=40`<br />雷达水平波束宽度 |
| RadarVerticalBeamwidth                                       | deg     | Radar beamwidth in elevation <br />`RadarVerticalBeamwidth=12`<br />雷达垂直波束宽度 |
| RadarRangeGateAzimuth                                        | deg     | Radar Range Gate azimuth (heading) relative to aircraft orientation `RadarRangeGateAzimuth=-20`<br />雷达测距方位角（相对于飞机方向的航向） |
| RadarRangeGateElevation                                      | deg     | Radar Range Gate elevation relative to aircraft orientation <br />`RadarRangeGateElevation=15`<br />雷达测距俯仰角（相对于飞机方向的俯仰） |
| RadarRangeGateRoll                                           | deg     | Radar Range Gate roll angle relative to aircraft orientation `RadarRangeGateRoll=-45`<br />雷达测距滚转角（相对于飞机方向的滚转） |
| RadarRangeGateMin                                            | m       | Defines the beginning of the range currently focused on by the radar (not to be confused with RadarRange). `RadarRangeGateMin=37040`<br />雷达测距最小距离（即雷达当前关注的范围的开头，不要与RadarRange混淆） |
| RadarRangeGateMax                                            | m       | Defines the end of the range currently focused on by the radar (not to be confused with RadarRange). <br />`RadarRangeGateMax=74080`<br />雷达测距最大距离（即雷达当前关注的范围的结尾，不要与RadarRange混淆） |
| RadarRangeGateHorizontalBeamwidth                            | deg     | Radar Range Gate beamwidth in azimuth <br />`RadarRangeGateHorizontalBeamwidth=40`<br />雷达测距水平波束宽度 |
| RadarRangeGateVerticalBeamwidth                              | deg     | Radar Range Gate beamwidth in elevation <br />`RadarRangeGateVerticalBeamwidth=12`<br />雷达测距垂直波束宽度 |
| LockedTargetMode                                             | number  | Primary target lock mode (0 = no lock/no target) <br />`LockedTargetMode=1`<br />锁定目标模式（0 = 无锁/无目标） |
| LockedTargetAzimuth                                          | deg     | Primary target azimuth (heading) relative to aircraft orientation `LockedTargetAzimuth=14.5`<br />锁定目标方位角（相对于飞机方向的航向） |
| LockedTargetElevation                                        | deg     | Primary target elevation relative to aircraft orientation `LockedTargetElevation=0.9`<br />锁定目标俯仰角（相对于飞机方向的俯仰） |
| LockedTargetRange                                            | m       | Primary target distance to aircraft <br />`LockedTargetRange=17303`<br />锁定目标距离飞机的距离 |
| EngagementMode <br />EngagementMode2                         | number  | Enable/disable engagement range (such as when a SAM site turns off its radar) (0 = off) <br />`EngagementMode=1`<br />启用/禁用武器攻击范围（例如SAM站关闭其雷达时）（0 = 关闭） |
| EngagementRange EngagementRange2 VerticalEngagementRange VerticalEngagementRange2 | m       | Engagement range for anti-aircraft units. This is the radius of the sphere which will be displayed in the 3D view. Typically used for SAM and AAA units, but this can be also relevant to warships. EngagementRange=2500 You can optionally specify the vertical engagement range to draw an ovoid engagement bubble. <br />`VerticalEngagementRange=1800`<br />指定反空袭单位的攻击范围。这是在3D视图中显示的球体的半径。通常用于SAM和AAA单位，但这对于战舰也可能是相关的。<br />您可以选择指定垂直攻击范围，以绘制一个卵形的攻击范围泡。 |
| RollControlInput <br />PitchControlInput <br />YawControlInput | ratio   | Raw player HOTAS/Yoke position in real-life (flight sim input device) <br />`PitchControlInput=0.41`<br />原始玩家HOTAS /Yoke的位置（飞行模拟器输入设 *[*16:23*]*备） |
| RollControlPosition PitchControlPosition YawControlPosition  | ratio   | HOTAS/Yoke position in simulated (with response curves) or real-life cockpit <br />`PitchControlPosition=0.3`<br /><br />HOTAS/操纵杆在模拟（带响应曲线）或实际驾驶舱中的位置。 |
| RollTrimTab <br />PitchTrimTab <br />YawTrimTab              | ratio   | Trim position for each axis <br />`PitchTrimTab=-0.15`<br />每一轴的微调位置 |
| AileronLeft<br />AileronRight <br />Elevator <br />Rudder    | ratio   | Control surfaces position on the aircraft <br />`Elevator=0.15`<br />飞机控制面的位置 |
| PilotHeadRoll <br />PilotHeadPitch<br />PilotHeadYaw         | deg     | Pilot head orientation in the cockpit relative to the aircraft orientation <br />`PilotHeadPitch=12`<br />驾驶员头部在驾驶舱内相对飞机方向的定位 |
| VerticalGForce <br />LongitudinalGForce <br />LateralGForce  | g       | Gravitational force equivalent of the acceleration in each axis relative to the aircraft orientation <br />`VerticalGForce=3.4`<br />相对于飞机方向的每个轴向加速度的重力相当于力量 |
| TriggerPressed                                               | boolean | Position of the main weapon trigger position. Set to 1.0 when the trigger is being fully pressed. All other values (such as 0.0) are considered as released. You could use continuous values from 0.0 to 1.0 to display the course of the trigger during time. <br />`TriggerPressed=1`<br />主武器扳机的位置。当扳机完全按下时，设置为1.0。所有其他值（例如0.0）都被视为已释放。您可以使用从0.0到1.0的连续值来显示扳机在时间上的进展。 |
| ENL                                                          | ratio   | Ratio between 0 and 1 describing the current Environmental Noise Level measured by the flight recorder. Typically used by gliders to detect engine use. This is the equivalent of the ENL field which can be found in IGC files. <br />`ENL=0.02`<br /><br />当量噪声级（Equivalent Noise Level）<br />比率在0和1之间，描述了飞行记录仪测量的当前环境噪声水平。通常用于滑翔机检测发动机使用。这相当于在IGC文件中可以找到的ENL字段。 |
| HeartRate                                                    | number  | Heart rate in beats per minute. <br />`HeartRate=72`<br />每分钟心跳次数。 |
| SpO2                                                         | ratio   | Blood oxygen saturation (SpO2) is the percentage of blood that is saturated with oxygen. <br />`SpO2=0.95`<br />血氧饱和度（SpO2）是血液中氧气的占比百分比。 |

#### Object Types (aka Tags)

Object types are now defined using a free combination of tags. The more tags, the more accurately an object is defined. Tags are separated by the plus sign +. Here are some examples:

> 对象类型现在使用标签的自由组合定义。标签越多，对象的定义就越精确。标签之间用加号 + 分隔。以下是一些示例：

| Object Kind                    | Type (Tags)                               |
| :----------------------------- | :---------------------------------------- |
| Aircraft Carrier<br />航空母舰 | Type=Heavy+Sea+Watercraft+AircraftCarrier |
| F-16C                          | Type=Medium+Air+FixedWing                 |
| Bicycle                        | Type=Light+Ground+Vehicle                 |
| AIM-120C                       | Type=Medium+Weapon+Missile                |
| Waypoint<br />航路点           | Type=Navaid+Static+Waypoint               |

Here is the list of currently supported tags. Tacview will use them for display and analysis purposes.

| Use            | Tags                                                         |
| :------------- | :----------------------------------------------------------- |
| Class          | Air<br />Ground<br />Sea<br />Weapon<br />Sensor<br />Navaid<br />Misc |
| Attributes     | Static<br />Heavy<br />Medium<br />Light<br />Minor          |
| Basic Types    | FixedWing<br />Rotorcraft<br />Armor<br />AntiAircraft<br />Vehicle<br />Watercraft<br />Human<br />Biologic<br />Missile<br />Rocket<br />Bomb<br />Torpedo<br />Projectile<br />Beam<br />Decoy<br />Building<br />Bullseye<br />Waypoint |
| Specific Types | Tank<br />Warship<br />AircraftCarrier<br />Submarine<br />Infantry<br />Parachutist<br />Shell<br />Bullet<br />Grenade<br />Flare<br />Chaff<br />SmokeGrenade<br />Aerodrome<br />Container<br />Shrapnel<br />Explosion |

> Air 空中：包括所有的飞行器，例如战斗机、准航空器等
>
> Ground 地面：包括所有的陆地载具，例如坦克、汽车等。
>
> Sea 海上：包括所有的水面载具，例如船、艇等。
>
> Weapon 武器：包括所有的武器，例如枪械、导弹等。
>
> Sensor 传感器：包括所有的传感器设备，例如雷达、红外线探测器等。
>
> Navaid 导航设备：包括所有的导航设备，例如GPS、气象雷达等。
>
> Misc 杂项：其他未分类的物品和设备。 

> Static 静态：指所有固定不动的物品，例如建筑物、固定桥梁等。
>
> Heavy 重型：指体积和重量较大的载具，例如坦克、飞机等。
>
> Medium 中型：指体积和重量适中的载具，例如汽车、轻型直升机等。
>
> Light 轻型：指体积和重量较小的载具，例如摩托车、小型轻型直升机等。
>
> Minor 细小：指非常小的装备或者零件。
>
> FixedWing 固定翼：指固定翼飞机。
>
> Rotorcraft 旋翼飞机：指直升机等旋翼飞机。
>
> Armor 装甲：指有防护装甲的装备，例如坦克、人员输送车等。
>
> AntiAircraft 防空：指用于格挡空中攻击的武器或装置，例如高射炮、SAM等。
>
> Vehicle 陆上载具：指所有在地上行驶的载具，例如汽车、坦克等。
>
> Watercraft 水上载具：指所有在水面行驶的载具，例如船只、艇等。
>
> Human 人类：指所有具有人形特征的生物。
>
> Biologic 生物：指所有非人形的生物。
>
> Missile 导弹：指用于空中、地面或者水面攻击的导弹。
>
> Rocket 火箭：指用于空中、地面或者水面攻击的火箭弹。
>
> Bomb 炸弹：指用于空中、地面或者水面攻击的炸弹。
>
> Torpedo 鱼雷：指用于水面或者水下攻击的鱼雷。
>
> Projectile 弹药：指所有射出或者抛出的攻击性装备，例如炮弹、火箭弹等。
>
> Beam 光束：指用于空中、地面或者水面攻击的光束武器。
>
> Decoy 诱饵：指用于扰乱敌方攻击的装备，例如钝化弹、音频干扰器等。
>
> Building 建筑物：指用于住宿、储存、机场、海港等地方的建筑物。
>
> Bullseye 靶标：指用于测试武器攻击效果的靶标。
>
> Waypoint 路径点：飞行员可以设置的导航点。

> Tank 坦克：指属于陆上车辆中的主战坦克。
>
> Warship 战舰：指属于水面舰艇中的战舰。
>
> AircraftCarrier 航空母舰：指属于水面舰艇中的航空母舰。
>
> Submarine 潜艇：指属于水下舰艇中的潜艇。
>
> Infantry 步兵：指步行进行作战和战斗的士兵。
>
> Parachutist 跳伞兵：指通过跳伞方式进行作战、突袭和侦察的士兵。
>
> Shell 炮弹：指用于射出的炮弹。
>
> Bullet 子弹：指用于射击的子弹。
>
> Grenade 手榴弹：指用于手持攻击的手榴弹。
>
> Flare 闪光弹：指用于发光来瞄准和误导目标的闪光弹。
>
> Chaff 金属箔：指用于扰乱敌方雷达或者传感器的金属箔。
>
> SmokeGrenade 烟雾弹：指用于制造浓烟雾来掩护自己行动的烟雾弹。
>
> Aerodrome 航空场：指飞机、直升机等航空器停靠、加油和维修的场地。
>
> Container 容器：指存放物品的容器，例如框架、箱子等。
>
> Shrapnel 炮弹碎片：指用于炮弹爆炸后散落的碎片。
>
> Explosion 爆炸：指所有的爆炸效果。



Here are the recommended common types (combination of tags) you should use to describe most of your objects for display in Tacview 1.x:


| Type                           | Tags                                       |
| :----------------------------- | :----------------------------------------- |
| Plane                          | Air + FixedWing                            |
| Helicopter                     | Air + Rotorcraft                           |
| Anti-Aircraft<br />防空        | Ground + AntiAircraft                      |
| Armor<br />装甲车              | Ground + Heavy + Armor + Vehicle           |
| Tank                           | Ground + Heavy + Armor + Vehicle + Tank    |
| Ground Vehicle<br />陆上车辆   | Ground + Vehicle                           |
| Watercraft<br />船             | Sea + Watercraft                           |
| Warship<br />军舰              | Sea + Watercraft + Warship                 |
| Aircraft Carrier<br />航空母舰 | Sea + Watercraft + AircraftCarrier         |
| Submarine<br />潜水艇          | Sea + Watercraft + Submarine               |
| Sonobuoy<br />声呐浮标         | Sea + Sensor                               |
| Human                          | Ground + Light + Human                     |
| Infantry<br />步兵             | Ground + Light + Human + Infantry          |
| Parachutist<br />伞兵          | Ground + Light + Human + Air + Parachutist |
| Missile                        | Weapon + Missile                           |
| Rocket                         | Weapon + Rocket                            |
| Bomb                           | Weapon + Bomb                              |
| Projectile<br />弹丸           | Weapon + Projectile                        |
| Beam<br />射线                 | Weapon + Beam                              |
| Shell<br />炮弹                | Projectile + Shell                         |
| Bullet<br />子弹               | Projectile + Bullet                        |
| Ballistic Shell<br />手榴弹    | Projectile + Shell + Heavy                 |
| Grenade                        | Projectile + Grenade                       |
| Decoy                          | Misc + Decoy                               |
| Flare                          | Misc + Decoy + Flare                       |
| Chaff                          | Misc + Decoy + Chaff                       |
| Smoke Grenade                  | Misc + Decoy + SmokeGrenade                |
| Building                       | Ground + Static + Building                 |
| Aerodrome                      | Ground + Static + Aerodrome                |
| Bullseye                       | Navaid + Static + Bullseye                 |
| Waypoint                       | Navaid + Static + Waypoint                 |
| Container                      | Misc + Container                           |
| Shrapnel                       | Misc + Shrapnel                            |
| Minor Object                   | Misc + Minor                               |
| Explosion                      | Misc + Explosion                           |

> Plane 飞机：指所有的固定翼飞行器，例如战斗机、运输机等。 
> Helicopter 直升机：指所有的旋翼飞行器，例如直升机、救援机等。 
> Anti-Aircraft 防空：指用于格挡空中攻击的武器或装置，例如高射炮、导弹等。 
> Armor 装甲：指有防护装甲的装备，例如坦克、人员输送车等。 
> Tank 坦克：指属于陆上车辆中的主战坦克。 
> Ground Vehicle 地面载具：指所有在地上行驶的载具，例如汽车、陆地警车等。 
> Watercraft 水上载具：指所有在水面行驶的载具，例如船只、艇等。 
> Warship 战舰：指属于水面舰艇中的战舰。 
> Aircraft Carrier 航空母舰：指属于水面舰艇中的航空母舰。 
> Submarine 潜艇：指属于水下舰艇中的潜艇。 
> Sonobuoy 声呐浮标：一种设备，用于在海洋中监听声波和水下噪音。 
> Human 人类：指所有具有人形特征的生物。 
> Infantry 步兵：指步行进行作战和战斗的士兵。 
> Parachutist 跳伞兵：指通过跳伞方式进行作战、突袭和侦察的士兵。 
> Missile 导弹：指可以自主或受控制地航行到目标并进行攻击的武器。 
> Rocket 火箭：指一种自身推进的弹药。 
> Bomb 炸弹：指一种被投掷、投射或布置在地面上目的是对敌方目标进行爆炸性打击的装备。 
> Projectile 光束：指用于空中、地面或者水面攻击的光束武器。 
> Beam 炮弹：指用于射出的炮弹。 
> Shell 子弹：指用于射击的子弹。 
> Bullet 弹药：指所有射出或者抛出的攻击性装备，例如炮弹、火箭弹等。 
> Ballistic Shell 弹药：指所有射出或者抛出的攻击性装备，例如炮弹、火箭弹等。 
> Grenade 手榴弹：指用于手持攻击的手榴弹。 
> Decoy 诱饵：指用于扰乱敌方攻击的装备，例如钝化弹、音频干扰器等。 
> Flare 闪光弹：指用于发光来瞄准和误导目标的闪光弹。 
> Chaff 金属箔：指用于扰乱敌方雷达或者传感器的金属箔。 
> Smoke Grenade 烟雾弹：指用于制造浓烟雾来掩护自己行动的烟雾弹。 
> Building 建筑物：指用于住宿、储存、机场、海港等地方的建筑物。 
> Aerodrome 航空场：指飞机、直升机等航空器停靠、加油和维修的场地。 
> Bullseye 靶标：指用于测试武器攻击效果的靶标。 
> Waypoint 路径点：飞行员可以设置的导航点。 
> Container 容器：指存放物品的容器，例如框架、箱子等。 
> Shrapnel 炮弹碎片：指用于炮弹爆炸后散落的碎片。
> Minor Object 细小物体：指体积和重量都非常小的物品。
> Explosion 爆炸：指所有的爆炸效果。



### Comments

To help you during the debugging process of your exporter, it is possible to comment any line of the file by prefixing them with the double slash // like in C++.

```
// This line and the following are commented
// 3000102,T=41.6251307|41.5910417|2000.14,Name=C172
```

These lines will be ignored by Tacview when loading the file. Comments are not preserved. You will notice that they are discarded the next time you save the file from Tacview. If you want to include debug information which is preserved, you can use the dedicated Debug Event described earlier in the global properties.

> 在加载文件时，Tacview将忽略这些行。注释不保留。您将注意到，下次从Tacview保存文件时，它们将被丢弃。如果希望包含保留的调试信息，可以使用前面在全局属性中描述的专用调试事件。

Because of loading performance considerations, it is only possible to insert a comment at the beginning of a line.

> 出于加载性能的考虑，只能在行首插入注释。
